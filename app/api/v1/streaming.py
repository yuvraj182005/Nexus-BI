import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_db_session
from app.models.identity import User
from app.streaming.schemas import (
    StreamIngestEvent,
    StreamingStatusResponse,
    WindowAggregationRequest,
)
from app.streaming.service import global_streaming_engine
from app.streaming.ws import ws_streaming_manager

router = APIRouter()
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/workspaces/{workspace_id}/streaming/ingest")
async def ingest_stream_event(
    workspace_id: uuid.UUID,
    event: StreamIngestEvent,
    user: CurrentUser,
) -> dict:
    res = global_streaming_engine.ingest_event(event)
    await ws_streaming_manager.push_live_update(
        str(workspace_id),
        {"type": "live_stream_update", "event": event.model_dump(mode="json")},
    )
    return res


@router.post("/workspaces/{workspace_id}/streaming/window-aggregate")
async def compute_window_aggregation(
    workspace_id: uuid.UUID,
    request: WindowAggregationRequest,
    user: CurrentUser,
) -> dict:
    return global_streaming_engine.compute_window_aggregation(request)


@router.get("/workspaces/{workspace_id}/streaming/status", response_model=StreamingStatusResponse)
async def get_streaming_status(
    workspace_id: uuid.UUID,
    user: CurrentUser,
) -> StreamingStatusResponse:
    return global_streaming_engine.get_status()


@router.websocket("/ws/streaming/{workspace_id}")
async def streaming_websocket_endpoint(websocket: WebSocket, workspace_id: str):
    await ws_streaming_manager.connect(workspace_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await ws_streaming_manager.push_live_update(workspace_id, data)
    except WebSocketDisconnect:
        ws_streaming_manager.disconnect(workspace_id, websocket)
