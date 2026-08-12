import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.collaboration.schemas import (
    CommentCreateRequest,
    CommentResponse,
    PresenceUpdate,
    TaskAssignRequest,
    TaskResponse,
)
from app.collaboration.service import global_collaboration_service
from app.collaboration.ws import ws_collaboration_manager
from app.database.session import get_db_session
from app.models.identity import User

router = APIRouter()
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/workspaces/{workspace_id}/collaboration/comments", response_model=CommentResponse)
async def add_comment(
    workspace_id: uuid.UUID,
    request: CommentCreateRequest,
    user: CurrentUser,
) -> CommentResponse:
    comment = global_collaboration_service.add_comment(user.id, request)
    await ws_collaboration_manager.broadcast_to_workspace(
        str(workspace_id),
        {"type": "new_comment", "comment": comment.model_dump(mode="json")},
    )
    return comment


@router.post("/workspaces/{workspace_id}/collaboration/tasks", response_model=TaskResponse)
async def assign_task(
    workspace_id: uuid.UUID,
    request: TaskAssignRequest,
    user: CurrentUser,
) -> TaskResponse:
    task = global_collaboration_service.assign_task(request)
    await ws_collaboration_manager.broadcast_to_workspace(
        str(workspace_id),
        {"type": "task_assigned", "task": task.model_dump(mode="json")},
    )
    return task


@router.post("/workspaces/{workspace_id}/collaboration/presence", response_model=list[PresenceUpdate])
async def update_presence(
    workspace_id: uuid.UUID,
    request: PresenceUpdate,
    user: CurrentUser,
) -> list[PresenceUpdate]:
    updated_list = global_collaboration_service.update_presence(request)
    await ws_collaboration_manager.broadcast_to_workspace(
        str(workspace_id),
        {"type": "presence_update", "online_users": [p.model_dump(mode="json") for p in updated_list]},
    )
    return updated_list


@router.websocket("/ws/collaboration/{workspace_id}")
async def collaboration_websocket_endpoint(websocket: WebSocket, workspace_id: str):
    await ws_collaboration_manager.connect(workspace_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await ws_collaboration_manager.broadcast_to_workspace(workspace_id, data)
    except WebSocketDisconnect:
        ws_collaboration_manager.disconnect(workspace_id, websocket)
