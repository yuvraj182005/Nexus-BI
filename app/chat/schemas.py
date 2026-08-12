import uuid
from typing import Any

from pydantic import BaseModel, Field


class ChatSessionCreateRequest(BaseModel):
    dataset_id: uuid.UUID | None = Field(None, description="Optional target dataset ID for scoping context")
    title: str | None = Field(None, description="Title for chat thread")


class ChatSessionResponse(BaseModel):
    id: uuid.UUID
    workspace_id: uuid.UUID
    dataset_id: uuid.UUID | None
    title: str
    created_at: Any


class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="User prompt message")


class ChatMessageResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    sender_role: str
    content: str
    citations: list[dict[str, Any]]
    structured_payload: dict[str, Any] | None
