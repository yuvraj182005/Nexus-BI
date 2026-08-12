import re
import time
import uuid
from typing import Any

from app.collaboration.schemas import (
    CommentCreateRequest,
    CommentResponse,
    PresenceUpdate,
    TaskAssignRequest,
    TaskResponse,
)


class CollaborationService:
    def __init__(self) -> None:
        self._comments: list[CommentResponse] = []
        self._tasks: list[TaskResponse] = []
        self._presence: dict[str, PresenceUpdate] = {}

    def add_comment(self, author_id: uuid.UUID, request: CommentCreateRequest) -> CommentResponse:
        mentions = re.findall(r"@(\w+)", request.content)
        c = CommentResponse(
            id=uuid.uuid4().hex,
            target_type=request.target_type,
            target_id=request.target_id,
            author_id=author_id,
            content=request.content,
            mentions=mentions,
            created_at=time.time(),
        )
        self._comments.append(c)
        return c

    def assign_task(self, request: TaskAssignRequest) -> TaskResponse:
        t = TaskResponse(
            id=uuid.uuid4().hex,
            title=request.title,
            assignee_id=request.assignee_id,
            target_type=request.target_type,
            target_id=request.target_id,
        )
        self._tasks.append(t)
        return t

    def update_presence(self, presence: PresenceUpdate) -> list[PresenceUpdate]:
        self._presence[str(presence.user_id)] = presence
        return list(self._presence.values())

    @staticmethod
    def compare_versions(v1_data: dict[str, Any], v2_data: dict[str, Any]) -> dict[str, Any]:
        added = {k: v for k, v in v2_data.items() if k not in v1_data}
        removed = {k: v for k, v in v1_data.items() if k not in v2_data}
        modified = {k: {"old": v1_data[k], "new": v2_data[k]} for k in v1_data if k in v2_data and v1_data[k] != v2_data[k]}
        return {"added": added, "removed": removed, "modified": modified}


global_collaboration_service = CollaborationService()
