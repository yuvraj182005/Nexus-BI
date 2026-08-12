import asyncio
import json
import math
import uuid
from pathlib import Path
from typing import Any

import pandas as pd
from pandas.api import types as pandas_types
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.models.dataset import DatasetVersion, DatasetVersionStatus
from app.models.profile import DatasetProfileReport, ProfileStatus
from app.repositories.profile import ProfileRepository
from app.storage.local import LocalObjectStorage


class ProfilingService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.storage = LocalObjectStorage(settings.local_storage_path)

    async def generate(self, version_id: uuid.UUID) -> DatasetProfileReport | None:
        version = await self.session.get(DatasetVersion, version_id)
        if not version or version.status != DatasetVersionStatus.READY:
            return None
        report = await ProfileRepository(self.session).get_for_dataset(version.dataset_id, version.id)
        if report is None:
            report = DatasetProfileReport(dataset_id=version.dataset_id, dataset_version_id=version.id)
            self.session.add(report)
            await self.session.flush()
        report.status = ProfileStatus.PROCESSING
        await self.session.commit()
        try:
            frame = await asyncio.to_thread(
                self._read_frame, self.storage.path_for(version.storage_key), version.format
            )
            values = await asyncio.to_thread(self._profile_frame, frame)
            self._apply(report, values)
            report.status = ProfileStatus.READY
            report.error_message = None
        except Exception as exc:
            report.status = ProfileStatus.FAILED
            report.error_message = str(exc)[:2000]
        await self.session.commit()
        if report.status == ProfileStatus.READY:
            from app.services.semantic import SemanticService

            await SemanticService(self.session, self.settings).generate(version.id)
        return report

    @staticmethod
    def _apply(report: DatasetProfileReport, values: dict[str, Any]) -> None:
        for key, value in values.items():
            if hasattr(report, key):
                setattr(report, key, value)

    @classmethod
    def _profile_frame(cls, frame: pd.DataFrame) -> dict[str, Any]:
        row_count, column_count = frame.shape
        total_cells = max(row_count * column_count, 1)
        missing_values = int(frame.isna().sum().sum())
        duplicate_rows = int(frame.duplicated().sum())
        duplicate_columns = cls._duplicate_column_count(frame)
        completeness = cls._score(1 - missing_values / total_cells)
        consistency = cls._score(1 - duplicate_rows / max(row_count, 1))
        uniqueness = cls._score(1 - duplicate_rows / max(row_count, 1))
        validity = cls._validity_score(frame)
        quality = cls._score(
            (completeness + consistency + uniqueness + validity) / 4
        )
        columns = [cls._column_profile(frame[column]) for column in frame.columns]
        correlations = cls._correlations(frame)
        relationships = cls._relationships(frame)
        distributions = {
            str(column): cls._distribution(frame[column]) for column in frame.columns
        }
        report = {
            "rows": int(row_count),
            "columns": int(column_count),
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "duplicate_columns": duplicate_columns,
            "quality_score": quality,
            "completeness_score": completeness,
            "consistency_score": consistency,
            "validity_score": validity,
            "uniqueness_score": uniqueness,
            "overall_health_score": quality,
            "column_profiles": columns,
            "correlations": correlations,
            "relationships": relationships,
            "data_distribution": distributions,
        }
        metrics = dict(report)
        report["report_json"] = {
            "summary": {
                "rows": int(row_count),
                "columns": int(column_count),
                "quality_score": quality,
                "overall_health_score": quality,
            },
            "metrics": metrics,
        }
        return report

    @staticmethod
    def _column_profile(series: pd.Series) -> dict[str, Any]:
        values = series.dropna()
        profile: dict[str, Any] = {
            "name": str(series.name),
            "data_type": str(series.dtype),
            "nullable": bool(series.isna().any()),
            "missing_count": int(series.isna().sum()),
            "missing_ratio": round(float(series.isna().mean()), 6),
            "unique_count": int(series.nunique(dropna=True)),
            "cardinality_ratio": round(float(series.nunique(dropna=True) / max(len(values), 1)), 6),
            "sample_values": [ProfilingService._json_value(value) for value in values.head(5).tolist()],
        }
        if pandas_types.is_numeric_dtype(series):
            numeric = pd.to_numeric(series, errors="coerce").dropna()
            profile["numerical_summary"] = {
                "min": ProfilingService._json_value(numeric.min()),
                "max": ProfilingService._json_value(numeric.max()),
                "mean": ProfilingService._json_value(numeric.mean()),
                "median": ProfilingService._json_value(numeric.median()),
                "std": ProfilingService._json_value(numeric.std()),
                "outlier_count": ProfilingService._outlier_count(numeric),
            }
        elif pandas_types.is_datetime64_any_dtype(series) or ProfilingService._looks_like_dates(series):
            date_values = series if pandas_types.is_datetime64_any_dtype(series) else pd.to_datetime(
                series, errors="coerce"
            )
            profile["date_summary"] = {
                "min": ProfilingService._json_value(date_values.min()),
                "max": ProfilingService._json_value(date_values.max()),
                "unique_days": int(date_values.dt.date.nunique()) if len(date_values) else 0,
            }
        else:
            counts = values.astype(str).value_counts().head(10)
            profile["categorical_summary"] = {
                "top_values": {str(key): int(value) for key, value in counts.items()},
                "category_count": int(values.nunique()),
            }
        return profile

    @staticmethod
    def _distribution(series: pd.Series) -> dict[str, Any]:
        if pandas_types.is_numeric_dtype(series):
            numeric = pd.to_numeric(series, errors="coerce").dropna()
            if numeric.empty:
                return {"kind": "numerical", "histogram": {}}
            histogram = numeric.value_counts(bins=10, sort=False)
            return {
                "kind": "numerical",
                "histogram": {str(interval): int(count) for interval, count in histogram.items()},
            }
        counts = series.dropna().astype(str).value_counts().head(20)
        return {"kind": "categorical", "values": {str(key): int(value) for key, value in counts.items()}}

    @staticmethod
    def _outlier_count(series: pd.Series) -> int:
        if series.empty:
            return 0
        first_quartile, third_quartile = series.quantile([0.25, 0.75])
        spread = third_quartile - first_quartile
        if pd.isna(spread) or spread == 0:
            return 0
        return int(((series < first_quartile - 1.5 * spread) | (series > third_quartile + 1.5 * spread)).sum())

    @staticmethod
    def _duplicate_column_count(frame: pd.DataFrame) -> int:
        return int(frame.T.duplicated().sum()) if not frame.empty else 0

    @staticmethod
    def _looks_like_dates(series: pd.Series) -> bool:
        if series.empty or pandas_types.is_numeric_dtype(series):
            return False
        parsed = pd.to_datetime(series.dropna(), errors="coerce")
        return bool(len(parsed) >= 2 and parsed.notna().mean() >= 0.8)

    @staticmethod
    def _validity_score(frame: pd.DataFrame) -> float:
        invalid = 0
        numeric_cells = 0
        for column in frame.select_dtypes(include="number"):
            values = frame[column].dropna()
            numeric_cells += len(values)
            invalid += int((~pd.Series(values).map(math.isfinite)).sum())
        return ProfilingService._score(1 - invalid / max(numeric_cells, 1))

    @staticmethod
    def _correlations(frame: pd.DataFrame) -> dict[str, dict[str, float]]:
        numeric = frame.select_dtypes(include="number")
        if numeric.empty:
            return {}
        matrix = numeric.corr().fillna(0)
        return {
            str(column): {str(other): round(float(value), 6) for other, value in row.items()}
            for column, row in matrix.to_dict().items()
        }

    @staticmethod
    def _relationships(frame: pd.DataFrame) -> list[dict[str, Any]]:
        relationships = []
        for column in frame.columns:
            normalized = str(column).lower()
            if normalized.endswith("_id") or normalized == "id":
                unique = frame[column].dropna().nunique()
                relationships.append(
                    {
                        "column": str(column),
                        "candidate": "primary_key" if unique == frame[column].notna().sum() else "foreign_key",
                        "confidence": round(float(unique / max(len(frame[column].dropna()), 1)), 6),
                    }
                )
        return relationships

    @staticmethod
    def _score(value: float) -> float:
        return round(max(0.0, min(1.0, float(value))) * 100, 4)

    @staticmethod
    def _json_value(value: Any) -> Any:
        if pd.isna(value):
            return None
        if isinstance(value, (pd.Timestamp,)):
            return value.isoformat()
        if hasattr(value, "item"):
            return value.item()
        return value

    @staticmethod
    def _read_frame(path: Path, file_format: str) -> pd.DataFrame:
        if file_format == "csv":
            return pd.read_csv(path)
        if file_format == "json":
            with path.open(encoding="utf-8") as file_handle:
                return pd.json_normalize(json.load(file_handle))
        if file_format in {"xlsx", "xls"}:
            return pd.read_excel(path)
        return pd.read_parquet(path)
