import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.jobs.orchestrator import JobOrchestrator
from app.jobs.schemas import JobCreateRequest, JobDashboardSummary, JobResponse, JobStatus
from app.models.job import BackgroundJobModel


class JobService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.orchestrator = JobOrchestrator(session)

    async def create_job(self, workspace_id: uuid.UUID, request: JobCreateRequest) -> JobResponse:
        job = await self.orchestrator.create_job(workspace_id, request.job_type, request.parent_job_id, request.parameters)
        return self._to_response(job)

    async def get_job(self, workspace_id: uuid.UUID, job_id: uuid.UUID) -> JobResponse:
        job = await self.session.get(BackgroundJobModel, job_id)
        if not job or job.workspace_id != workspace_id:
            raise ValueError("Job not found in this workspace")
        return self._to_response(job)

    async def cancel_job(self, workspace_id: uuid.UUID, job_id: uuid.UUID) -> JobResponse:
        job = await self.orchestrator.cancel_job(job_id)
        if not job or job.workspace_id != workspace_id:
            raise ValueError("Job not found in this workspace")
        return self._to_response(job)

    async def list_jobs(self, workspace_id: uuid.UUID, status_filter: str | None = None) -> list[JobResponse]:
        query = select(BackgroundJobModel).where(BackgroundJobModel.workspace_id == workspace_id)
        if status_filter:
            query = query.where(BackgroundJobModel.status == status_filter)
        query = query.order_by(BackgroundJobModel.created_at.desc())

        result = await self.session.scalars(query)
        return [self._to_response(j) for j in result.all()]

    async def get_dashboard_summary(self, workspace_id: uuid.UUID) -> JobDashboardSummary:
        all_jobs = await self.list_jobs(workspace_id)
        counts = {
            "queued": sum(1 for j in all_jobs if j.status == JobStatus.QUEUED),
            "running": sum(1 for j in all_jobs if j.status == JobStatus.RUNNING),
            "completed": sum(1 for j in all_jobs if j.status == JobStatus.COMPLETED),
            "failed": sum(1 for j in all_jobs if j.status == JobStatus.FAILED),
            "cancelled": sum(1 for j in all_jobs if j.status == JobStatus.CANCELLED),
        }
        return JobDashboardSummary(
            total_jobs=len(all_jobs),
            queued=counts["queued"],
            running=counts["running"],
            completed=counts["completed"],
            failed=counts["failed"],
            cancelled=counts["cancelled"],
            recent_jobs=all_jobs[:10],
        )

    @staticmethod
    def _to_response(job: BackgroundJobModel) -> JobResponse:
        return JobResponse(
            id=job.id,
            workspace_id=job.workspace_id,
            job_type=job.job_type,
            status=JobStatus(job.status) if job.status in JobStatus.__members__.values() else JobStatus.QUEUED,
            progress_percent=job.progress_percent,
            retry_count=job.retry_count,
            parent_job_id=None,
            child_job_ids=[],
            worker="celery_worker_1",
            logs=job.logs or [],
            error_message=job.error_message,
            result_metadata=job.result_metadata,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
