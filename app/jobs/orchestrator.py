import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.jobs.schemas import JobStatus
from app.models.job import BackgroundJobModel


class JobOrchestrator:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_job(
        self,
        workspace_id: uuid.UUID,
        job_type: str,
        parent_job_id: uuid.UUID | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> BackgroundJobModel:
        job = BackgroundJobModel(
            workspace_id=workspace_id,
            job_type=job_type,
            status=JobStatus.QUEUED,
            progress_percent=0.0,
            retry_count=0,
            logs=[f"[Job Created] Type={job_type} Queued for Celery execution."],
            result_metadata={"parameters": parameters or {}},
        )
        self.session.add(job)
        await self.session.commit()
        return job

    async def update_progress(
        self, job_id: uuid.UUID, progress: float, log_entry: str | None = None, status: JobStatus | None = None
    ) -> BackgroundJobModel | None:
        job = await self.session.get(BackgroundJobModel, job_id)
        if not job:
            return None

        job.progress_percent = min(100.0, max(0.0, progress))
        if status:
            job.status = status

        logs = list(job.logs or [])
        if log_entry:
            logs.append(log_entry)
        job.logs = logs

        await self.session.commit()
        return job

    async def cancel_job(self, job_id: uuid.UUID) -> BackgroundJobModel | None:
        job = await self.session.get(BackgroundJobModel, job_id)
        if not job:
            return None

        job.status = JobStatus.CANCELLED
        logs = list(job.logs or [])
        logs.append("[Job Cancelled] Execution stopped by user request.")
        job.logs = logs

        await self.session.commit()
        return job
