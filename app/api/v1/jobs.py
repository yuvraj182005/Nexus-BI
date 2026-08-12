import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.jobs.schemas import JobCreateRequest, JobDashboardSummary, JobResponse
from app.jobs.service import JobService
from app.models.identity import User, UserRole

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
JobManager = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))]


@router.get("/jobs", response_model=list[JobResponse])
async def list_jobs(
    workspace_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
    status_filter: str | None = None,
) -> list[JobResponse]:
    return await JobService(session, get_settings()).list_jobs(workspace_id, status_filter)


@router.get("/jobs/summary", response_model=JobDashboardSummary)
async def get_jobs_dashboard_summary(
    workspace_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
) -> JobDashboardSummary:
    return await JobService(session, get_settings()).get_dashboard_summary(workspace_id)


@router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    workspace_id: uuid.UUID,
    request: JobCreateRequest,
    session: Session,
    user: JobManager,
) -> JobResponse:
    return await JobService(session, get_settings()).create_job(workspace_id, request)


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job_detail(
    workspace_id: uuid.UUID,
    job_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
) -> JobResponse:
    try:
        return await JobService(session, get_settings()).get_job(workspace_id, job_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/jobs/{job_id}/cancel", response_model=JobResponse)
async def cancel_job(
    workspace_id: uuid.UUID,
    job_id: uuid.UUID,
    session: Session,
    user: JobManager,
) -> JobResponse:
    try:
        return await JobService(session, get_settings()).cancel_job(workspace_id, job_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
