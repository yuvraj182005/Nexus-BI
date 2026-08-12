import json
import uuid
from pathlib import Path

import pandas as pd
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.models.dataset import (
    Dataset,
    DatasetStatus,
    DatasetTag,
    DatasetVersion,
    DatasetVersionStatus,
)
from app.models.identity import User, Workspace
from app.repositories.dataset import DatasetRepository
from app.services.profiling import ProfilingService
from app.storage.local import LocalObjectStorage


class DatasetService:
    SUPPORTED_FORMATS = {"csv", "xlsx", "xls", "json", "parquet"}

    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.repository = DatasetRepository(session)
        self.storage = LocalObjectStorage(settings.local_storage_path)

    async def upload(
        self, user: User, workspace_id: uuid.UUID, upload: UploadFile, name: str, description: str | None, tags: list[str]
    ) -> tuple[Dataset, DatasetVersion, bool]:
        workspace = await self.session.scalar(
            select(Workspace).where(
                Workspace.id == workspace_id,
                Workspace.organization_id == user.organization_id,
                Workspace.is_active.is_(True),
            )
        )
        if not workspace:
            raise ValueError("Workspace not found")
        file_format = self._format(upload.filename)
        slug = self._slug(name)
        if await self.session.scalar(
            select(Dataset).where(Dataset.workspace_id == workspace_id, Dataset.slug == slug)
        ):
            raise ValueError("Dataset name already exists in this workspace")

        dataset = Dataset(
            organization_id=user.organization_id,
            workspace_id=workspace_id,
            owner_id=user.id,
            name=name,
            slug=slug,
            description=description,
            status=DatasetStatus.PROCESSING,
        )
        self.session.add(dataset)
        await self.session.flush()
        version = DatasetVersion(
            dataset_id=dataset.id,
            version_number=1,
            status=DatasetVersionStatus.PROCESSING,
            original_filename=upload.filename or "dataset",
            format=file_format,
            content_type=upload.content_type,
            storage_key=f"{user.organization_id}/{workspace_id}/{dataset.id}/1.{file_format}",
            checksum_sha256="pending",
            file_size_bytes=0,
        )
        self.session.add(version)
        for tag in self._normalize_tags(tags):
            dataset.tags.append(DatasetTag(tag=tag))
        await self.session.flush()
        size, checksum = await self.storage.save_upload(version.storage_key, upload)
        version.file_size_bytes = size
        version.checksum_sha256 = checksum
        await self.session.commit()
        if version.status == DatasetVersionStatus.READY:
            await ProfilingService(self.session, self.settings).generate(version.id)
        process_async = size > self.settings.dataset_sync_max_bytes
        return dataset, version, process_async

    async def process_version(self, version_id: uuid.UUID) -> None:
        version = await self.session.get(DatasetVersion, version_id)
        if not version:
            return
        dataset = await self.session.get(Dataset, version.dataset_id)
        if not dataset:
            return
        try:
            frame = self._read_frame(self.storage.path_for(version.storage_key), version.format)
            version.row_count = int(frame.shape[0])
            version.column_count = int(frame.shape[1])
            version.schema_json = [
                {"name": str(column), "dtype": str(frame[column].dtype), "nullable": bool(frame[column].isna().any())}
                for column in frame.columns
            ]
            version.statistics_json = {
                "missing_values": {str(column): int(frame[column].isna().sum()) for column in frame.columns},
                "duplicate_rows": int(frame.duplicated().sum()),
            }
            version.validation_json = {"valid": True, "errors": []}
            version.status = DatasetVersionStatus.READY
            dataset.status = DatasetStatus.READY
            dataset.current_version_id = version.id
            dataset.metadata_json = {
                "row_count": version.row_count,
                "column_count": version.column_count,
                "format": version.format,
            }
        except Exception as exc:
            version.status = DatasetVersionStatus.FAILED
            version.error_message = str(exc)[:2000]
            dataset.status = DatasetStatus.FAILED
        await self.session.commit()
        if version.status == DatasetVersionStatus.READY:
            await ProfilingService(self.session, self.settings).generate(version.id)

    async def upload_version(self, dataset: Dataset, upload: UploadFile) -> tuple[DatasetVersion, bool]:
        file_format = self._format(upload.filename)
        version = DatasetVersion(
            dataset_id=dataset.id,
            version_number=await self.repository.next_version_number(dataset.id),
            status=DatasetVersionStatus.PROCESSING,
            original_filename=upload.filename or "dataset",
            format=file_format,
            content_type=upload.content_type,
            storage_key=f"{dataset.organization_id}/{dataset.workspace_id}/{dataset.id}/pending.{file_format}",
            checksum_sha256="pending",
            file_size_bytes=0,
        )
        self.session.add(version)
        await self.session.flush()
        version.storage_key = (
            f"{dataset.organization_id}/{dataset.workspace_id}/{dataset.id}/"
            f"{version.version_number}.{file_format}"
        )
        size, checksum = await self.storage.save_upload(version.storage_key, upload)
        version.file_size_bytes = size
        version.checksum_sha256 = checksum
        dataset.status = DatasetStatus.PROCESSING
        await self.session.commit()
        return version, size > self.settings.dataset_sync_max_bytes

    async def preview(self, version: DatasetVersion) -> tuple[list[str], list[dict], bool]:
        frame = self._read_frame(self.storage.path_for(version.storage_key), version.format)
        limit = self.settings.dataset_preview_rows
        rows = frame.head(limit).where(frame.notna(), None).to_dict(orient="records")
        return [str(column) for column in frame.columns], rows, len(frame) > limit

    @staticmethod
    def _format(filename: str | None) -> str:
        file_format = Path(filename or "").suffix.lower().lstrip(".")
        if file_format not in DatasetService.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported dataset format: {file_format or 'unknown'}")
        return file_format

    @staticmethod
    def _slug(value: str) -> str:
        slug = "-".join(value.lower().split())
        normalized = "".join(character for character in slug if character.isalnum() or character == "-")[:120]
        if not normalized:
            raise ValueError("Dataset name must contain letters or numbers")
        return normalized

    @staticmethod
    def _normalize_tags(tags: list[str]) -> list[str]:
        return sorted({tag.strip().lower() for tag in tags if tag.strip()})

    @staticmethod
    def _read_frame(path: Path, file_format: str) -> pd.DataFrame:
        if file_format == "csv":
            return pd.read_csv(path)
        if file_format == "json":
            with path.open(encoding="utf-8") as file_handle:
                payload = json.load(file_handle)
            return pd.json_normalize(payload)
        if file_format in {"xlsx", "xls"}:
            return pd.read_excel(path)
        return pd.read_parquet(path)
