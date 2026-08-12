import json
import time
import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.audit.schemas import (
    AuditExportResponse,
    AuditLogRecord,
    AuditSearchRequest,
    AuditSearchResponse,
)
from app.core.config import Settings


class AuditService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self._memory_logs: list[AuditLogRecord] = []

    def record_activity(
        self,
        user_id: uuid.UUID,
        workspace_id: uuid.UUID,
        action: str,
        target: str,
        status: str = "success",
        duration_ms: float = 0.0,
        client_ip: str = "127.0.0.1",
        details: dict[str, Any] | None = None,
    ) -> AuditLogRecord:
        record = AuditLogRecord(
            timestamp=time.time(),
            user_id=user_id,
            workspace_id=workspace_id,
            client_ip=client_ip,
            action=action,
            target=target,
            status=status,
            duration_ms=duration_ms,
            details=details or {},
        )
        self._memory_logs.append(record)
        return record

    async def search_logs(self, workspace_id: uuid.UUID, request: AuditSearchRequest) -> AuditSearchResponse:
        filtered = [l for l in self._memory_logs if str(l.workspace_id) == str(workspace_id)]

        if request.user_id:
            filtered = [l for l in filtered if l.user_id == request.user_id]
        if request.actions:
            filtered = [l for l in filtered if l.action in request.actions]
        if request.status_filter:
            filtered = [l for l in filtered if l.status == request.status_filter]

        filtered.sort(key=lambda x: x.timestamp, reverse=True)
        return AuditSearchResponse(total_count=len(filtered), logs=filtered[: request.limit])

    async def export_logs(self, workspace_id: uuid.UUID, export_format: str = "json") -> AuditExportResponse:
        logs = [l.model_dump(mode="json") for l in self._memory_logs if str(l.workspace_id) == str(workspace_id)]
        if export_format == "csv":
            header = "id,timestamp,action,target,status,duration_ms,client_ip\n"
            lines = [f"{l['id']},{l['timestamp']},{l['action']},{l['target']},{l['status']},{l['duration_ms']},{l['client_ip']}" for l in logs]
            data = header + "\n".join(lines)
        else:
            data = json.dumps(logs, indent=2)

        return AuditExportResponse(
            export_format=export_format,
            export_url=f"/api/v1/workspaces/{workspace_id}/audit/export?format={export_format}",
            record_count=len(logs),
            data=data,
        )


# Global Audit Tracker instance
global_audit_service = AuditService(None, None)
