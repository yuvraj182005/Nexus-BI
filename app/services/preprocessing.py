import asyncio
import hashlib
import re
from pathlib import Path
from typing import Any

import pandas as pd
from pandas.api import types as pandas_types
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.models.dataset import Dataset, DatasetVersion, DatasetVersionStatus
from app.models.identity import User
from app.models.preprocessing import (
    PreprocessingOperation,
    PreprocessingRun,
    PreprocessingRunStatus,
    PreprocessingStep,
    PreprocessingStepDecision,
)
from app.repositories.dataset import DatasetRepository
from app.schemas.preprocessing import PreprocessingRunCreateRequest, PreprocessingStepRequest
from app.services.profiling import ProfilingService
from app.storage.local import LocalObjectStorage


class PreprocessingService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.storage = LocalObjectStorage(settings.local_storage_path)
        self.dataset_repository = DatasetRepository(session)

    async def recommendations(self, version: DatasetVersion) -> list[dict[str, Any]]:
        frame = await asyncio.to_thread(
            ProfilingService._read_frame, self.storage.path_for(version.storage_key), version.format
        )
        return await asyncio.to_thread(self._recommend_frame, frame)

    async def execute(
        self,
        user: User,
        dataset: Dataset,
        request: PreprocessingRunCreateRequest,
    ) -> PreprocessingRun:
        source_version = await self.dataset_repository.get_version(dataset, request.source_version_id)
        if not source_version or source_version.status != DatasetVersionStatus.READY:
            raise ValueError("Source dataset version is not ready")
        run = PreprocessingRun(
            dataset_id=dataset.id,
            source_version_id=source_version.id,
            initiated_by=user.id,
            status=PreprocessingRunStatus.PROCESSING,
        )
        self.session.add(run)
        await self.session.flush()
        try:
            frame = await asyncio.to_thread(
                ProfilingService._read_frame,
                self.storage.path_for(source_version.storage_key),
                source_version.format,
            )
            before_profile = await asyncio.to_thread(ProfilingService._profile_frame, frame)
            run.quality_before = before_profile["overall_health_score"]
            working = frame.copy()
            for index, requested in enumerate(request.steps, start=1):
                step = self._step_from_request(index, requested)
                before = self._snapshot(working)
                if requested.decision in {
                    PreprocessingStepDecision.REJECTED,
                    PreprocessingStepDecision.PENDING,
                }:
                    step.before_snapshot = before
                    step.after_snapshot = before
                    run.steps.append(step)
                    continue
                try:
                    working = self._apply_operation(working, requested)
                    step.decision = PreprocessingStepDecision.APPLIED
                    step.before_snapshot = before
                    step.after_snapshot = self._snapshot(working)
                except (KeyError, TypeError, ValueError) as exc:
                    step.decision = PreprocessingStepDecision.FAILED
                    step.error_message = str(exc)[:1000]
                    run.steps.append(step)
                    raise
                run.steps.append(step)
            output_version = await self._write_output(dataset, working, source_version)
            after_profile = await asyncio.to_thread(ProfilingService._profile_frame, working)
            run.quality_after = after_profile["overall_health_score"]
            run.output_version_id = output_version.id
            run.status = PreprocessingRunStatus.COMPLETED
            dataset.current_version_id = output_version.id
            dataset.status = "ready"
            await self.session.commit()
            await ProfilingService(self.session, self.settings).generate(output_version.id)
        except Exception as exc:
            run.status = PreprocessingRunStatus.FAILED
            run.error_message = str(exc)[:2000]
            await self.session.commit()
        return run

    async def undo(self, run: PreprocessingRun) -> PreprocessingRun:
        if run.status != PreprocessingRunStatus.COMPLETED:
            raise ValueError("Only completed preprocessing runs can be undone")
        dataset = await self.session.get(Dataset, run.dataset_id)
        if not dataset:
            raise ValueError("Dataset not found")
        dataset.current_version_id = run.source_version_id
        run.status = PreprocessingRunStatus.UNDONE
        run.undone_at = pd.Timestamp.utcnow().to_pydatetime()
        await self.session.commit()
        return run

    @classmethod
    def _recommend_frame(cls, frame: pd.DataFrame) -> list[dict[str, Any]]:
        recommendations: list[dict[str, Any]] = []
        duplicate_count = int(frame.duplicated().sum())
        if not duplicate_count:
            id_cols = [c for c in frame.columns if "id" in str(c).lower()]
            if id_cols:
                duplicate_count = int(frame.duplicated(subset=id_cols).sum())
        if duplicate_count:
            recommendations.append(
                cls._recommendation(
                    PreprocessingOperation.DROP_DUPLICATES,
                    None,
                    {},
                    f"Detected {duplicate_count} duplicate rows.",
                    0.99,
                    "high",
                    duplicate_count / max(len(frame), 1) * 100,
                )
            )
        for column in frame.columns:
            series = frame[column]
            missing = int(series.isna().sum())
            if missing:
                method = "median" if pandas_types.is_numeric_dtype(series) else "mode"
                recommendations.append(
                    cls._recommendation(
                        PreprocessingOperation.IMPUTE_MISSING,
                        str(column),
                        {"method": method},
                        f"Column contains {missing} missing values; {method} imputation preserves row count.",
                        0.92,
                        "high" if missing / max(len(frame), 1) > 0.1 else "medium",
                        missing / max(len(frame), 1) * 100,
                    )
                )
            if pandas_types.is_numeric_dtype(series):
                outliers = ProfilingService._outlier_count(pd.to_numeric(series, errors="coerce").dropna())
                if outliers:
                    recommendations.append(
                        cls._recommendation(
                            PreprocessingOperation.CLIP_OUTLIERS,
                            str(column),
                            {"method": "iqr"},
                            f"IQR analysis detected {outliers} potential outliers.",
                            0.86,
                            "medium",
                            outliers / max(len(frame), 1) * 100,
                        )
                    )
                recommendations.append(
                    cls._recommendation(
                        PreprocessingOperation.NORMALIZE_NUMERIC,
                        str(column),
                        {"method": "minmax"},
                        "Numeric scale can be normalized for downstream modeling.",
                        0.78,
                        "low",
                        2.0,
                    )
                )
            elif cls._looks_like_dates(series):
                recommendations.append(
                    cls._recommendation(
                        PreprocessingOperation.PARSE_DATES,
                        str(column),
                        {},
                        "Values are date-like and should be converted to a typed datetime column.",
                        0.9,
                        "medium",
                        5.0,
                    )
                )
            elif series.nunique(dropna=True) < max(len(frame) * 0.5, 20):
                recommendations.append(
                    cls._recommendation(
                        PreprocessingOperation.ENCODE_CATEGORICAL,
                        str(column),
                        {"method": "one_hot"},
                        "Low-cardinality text can be encoded for analytical and ML workflows.",
                        0.8,
                        "medium",
                        4.0,
                    )
                )
            if not re.fullmatch(r"[a-z][a-z0-9_]*", str(column)):
                recommendations.append(
                    cls._recommendation(
                        PreprocessingOperation.STANDARDIZE_COLUMNS,
                        str(column),
                        {},
                        "Column name is not in the platform standard snake_case format.",
                        0.98,
                        "low",
                        1.0,
                    )
                )
        return recommendations

    @staticmethod
    def _recommendation(operation, column_name, parameters, reason, confidence, impact, improvement):
        op_enum = PreprocessingOperation(operation) if isinstance(operation, str) else operation
        return {
            "operation": op_enum,
            "column_name": column_name,
            "parameters": parameters,
            "reason": reason,
            "confidence": round(confidence, 4),
            "impact": impact,
            "estimated_improvement": round(improvement, 4),
        }

    @staticmethod
    def _step_from_request(order: int, request: PreprocessingStepRequest) -> PreprocessingStep:
        return PreprocessingStep(
            step_order=order,
            operation=request.operation.value,
            column_name=request.column_name,
            decision=request.decision,
            parameters=request.parameters,
            reason="User-selected preprocessing operation",
            confidence=1.0,
            impact="user_defined",
            estimated_improvement=0.0,
        )

    @classmethod
    def _apply_operation(cls, frame: pd.DataFrame, request: PreprocessingStepRequest) -> pd.DataFrame:
        operation = request.operation
        column = request.column_name
        parameters = request.parameters
        if operation == PreprocessingOperation.DROP_DUPLICATES:
            return frame.drop_duplicates().reset_index(drop=True)
        if operation == PreprocessingOperation.IMPUTE_MISSING:
            cls._require_column(frame, column)
            method = parameters.get("method", "median")
            if method == "median":
                value = pd.to_numeric(frame[column], errors="coerce").median()
            elif method == "mode":
                modes = frame[column].mode(dropna=True)
                value = modes.iloc[0] if not modes.empty else "unknown"
            elif method == "constant":
                value = parameters.get("value")
            else:
                raise ValueError("Unsupported missing-value method")
            frame[column] = frame[column].fillna(value)
            return frame
        if operation == PreprocessingOperation.CLIP_OUTLIERS:
            cls._require_column(frame, column)
            numeric = pd.to_numeric(frame[column], errors="coerce")
            first, third = numeric.quantile([0.25, 0.75])
            spread = third - first
            if pd.notna(spread) and spread:
                frame[column] = numeric.clip(first - 1.5 * spread, third + 1.5 * spread)
            return frame
        if operation == PreprocessingOperation.PARSE_DATES:
            cls._require_column(frame, column)
            frame[column] = pd.to_datetime(frame[column], errors="coerce", utc=True)
            return frame
        if operation == PreprocessingOperation.STANDARDIZE_COLUMNS:
            rename = {str(name): cls._standard_name(str(name)) for name in frame.columns}
            standardized = list(rename.values())
            if len(standardized) != len(set(standardized)):
                raise ValueError("Column standardization would create duplicate column names")
            return frame.rename(columns=rename)
        if operation == PreprocessingOperation.ENCODE_CATEGORICAL:
            cls._require_column(frame, column)
            encoded = pd.get_dummies(frame[column], prefix=cls._standard_name(column or "value"), dtype=int)
            return pd.concat([frame.drop(columns=[column]), encoded], axis=1)
        if operation == PreprocessingOperation.NORMALIZE_NUMERIC:
            cls._require_column(frame, column)
            numeric = pd.to_numeric(frame[column], errors="coerce")
            minimum, maximum = numeric.min(), numeric.max()
            if pd.notna(minimum) and pd.notna(maximum) and maximum != minimum:
                frame[column] = (numeric - minimum) / (maximum - minimum)
            return frame
        if operation == PreprocessingOperation.DERIVE_RATIO:
            numerator = parameters.get("numerator")
            denominator = parameters.get("denominator")
            output = parameters.get("name")
            if not all(isinstance(value, str) for value in (numerator, denominator, output)):
                raise ValueError("derive_ratio requires numerator, denominator, and name")
            cls._require_column(frame, numerator)
            cls._require_column(frame, denominator)
            frame[output] = pd.to_numeric(frame[numerator], errors="coerce") / pd.to_numeric(
                frame[denominator], errors="coerce"
            ).replace(0, pd.NA)
            return frame
        if operation == PreprocessingOperation.VALIDATE_NOT_NULL:
            cls._require_column(frame, column)
            if frame[column].isna().any():
                raise ValueError(f"Not-null validation failed for column: {column}")
            return frame
        if operation == PreprocessingOperation.VALIDATE_RANGE:
            cls._require_column(frame, column)
            minimum = parameters.get("min")
            maximum = parameters.get("max")
            numeric = pd.to_numeric(frame[column], errors="coerce")
            invalid = pd.Series(False, index=frame.index)
            if minimum is not None:
                invalid |= numeric < minimum
            if maximum is not None:
                invalid |= numeric > maximum
            if invalid.any():
                raise ValueError(f"Range validation failed for column: {column}")
            return frame
        raise ValueError(f"Unsupported preprocessing operation: {operation}")

    async def _write_output(
        self, dataset: Dataset, frame: pd.DataFrame, source_version: DatasetVersion
    ) -> DatasetVersion:
        version_number = await self.dataset_repository.next_version_number(dataset.id)
        storage_key = f"{dataset.organization_id}/{dataset.workspace_id}/{dataset.id}/{version_number}.csv"
        path = self.storage.path_for(storage_key)
        path.parent.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(frame.to_csv, path, index=False)
        size, checksum = await asyncio.to_thread(self._file_stats, path)
        version = DatasetVersion(
            dataset_id=dataset.id,
            version_number=version_number,
            status=DatasetVersionStatus.READY,
            original_filename=f"preprocessed-v{version_number}.csv",
            format="csv",
            content_type="text/csv",
            storage_key=storage_key,
            checksum_sha256=checksum,
            file_size_bytes=size,
            row_count=int(frame.shape[0]),
            column_count=int(frame.shape[1]),
            schema_json=[
                {"name": str(column), "dtype": str(frame[column].dtype), "nullable": bool(frame[column].isna().any())}
                for column in frame.columns
            ],
            validation_json={"valid": True, "errors": []},
        )
        self.session.add(version)
        await self.session.flush()
        return version

    @staticmethod
    def _file_stats(path: Path) -> tuple[int, str]:
        digest = hashlib.sha256()
        size = 0
        with path.open("rb") as file_handle:
            while chunk := file_handle.read(1024 * 1024):
                digest.update(chunk)
                size += len(chunk)
        return size, digest.hexdigest()

    @staticmethod
    def _snapshot(frame: pd.DataFrame) -> dict[str, Any]:
        return {
            "rows": int(frame.shape[0]),
            "columns": int(frame.shape[1]),
            "missing_values": int(frame.isna().sum().sum()),
            "duplicate_rows": int(frame.duplicated().sum()),
            "column_names": [str(column) for column in frame.columns],
        }

    @staticmethod
    def _require_column(frame: pd.DataFrame, column: str | None) -> None:
        if not column or column not in frame.columns:
            raise KeyError(f"Column not found: {column or '<required>'}")

    @staticmethod
    def _standard_name(value: str) -> str:
        normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
        return normalized or "column"

    @staticmethod
    def _looks_like_dates(series: pd.Series) -> bool:
        if series.empty or pandas_types.is_numeric_dtype(series):
            return False
        parsed = pd.to_datetime(series.dropna(), errors="coerce")
        return bool(len(parsed) >= 2 and parsed.notna().mean() >= 0.8)
