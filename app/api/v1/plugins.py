import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.database.session import get_db_session
from app.models.identity import User, UserRole
from app.plugins.registry import global_plugin_registry
from app.plugins.schemas import PluginManifest, PluginRegisterRequest

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
PluginAdmin = Annotated[User, Depends(require_roles(UserRole.ADMIN))]


@router.get("/plugins", response_model=list[PluginManifest])
async def list_plugins(
    workspace_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
    plugin_type: str | None = None,
) -> list[PluginManifest]:
    return global_plugin_registry.list_plugins(plugin_type)


@router.post("/plugins/register", response_model=PluginManifest, status_code=status.HTTP_201_CREATED)
async def register_plugin(
    workspace_id: uuid.UUID,
    request: PluginRegisterRequest,
    session: Session,
    user: PluginAdmin,
) -> PluginManifest:
    try:
        return global_plugin_registry.register_plugin(request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/plugins/hot-reload")
async def hot_reload_plugins(
    workspace_id: uuid.UUID,
    session: Session,
    user: PluginAdmin,
) -> dict[str, Any]:
    count = global_plugin_registry.hot_reload()
    return {"status": "reloaded", "active_plugins_count": count}
