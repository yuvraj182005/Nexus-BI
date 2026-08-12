import uuid

from pydantic import BaseModel, Field


class CommentCreateRequest(BaseModel):
    target_type: str = Field(..., description="dashboard, report, workflow, dataset")
    target_id: str
    content: str = Field(..., description="Comment text, supporting @mentions")
    parent_comment_id: str | None = None


class CommentResponse(BaseModel):
    id: str
    target_type: str
    target_id: str
    author_id: uuid.UUID
    content: str
    mentions: list[str]
    created_at: float


class TaskAssignRequest(BaseModel):
    title: str
    assignee_id: uuid.UUID
    target_type: str
    target_id: str
    due_date: float | None = None


class TaskResponse(BaseModel):
    id: str
    title: str
    assignee_id: uuid.UUID
    status: str = "pending"  # pending, approved, rejected, completed
    target_type: str
    target_id: str


class PresenceUpdate(BaseModel):
    user_id: uuid.UUID
    user_name: str
    active_resource_id: str
    status: str = "online"  # online, away, editing
