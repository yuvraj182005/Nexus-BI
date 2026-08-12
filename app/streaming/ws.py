from fastapi import WebSocket


class StreamingWebSocketManager:
    def __init__(self) -> None:
        self.active_streams: dict[str, list[WebSocket]] = {}

    async def connect(self, workspace_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        if workspace_id not in self.active_streams:
            self.active_streams[workspace_id] = []
        self.active_streams[workspace_id].append(websocket)

    def disconnect(self, workspace_id: str, websocket: WebSocket) -> None:
        if workspace_id in self.active_streams:
            if websocket in self.active_streams[workspace_id]:
                self.active_streams[workspace_id].remove(websocket)

    async def push_live_update(self, workspace_id: str, update_payload: dict) -> None:
        if workspace_id in self.active_streams:
            for connection in self.active_streams[workspace_id]:
                await connection.send_json(update_payload)


ws_streaming_manager = StreamingWebSocketManager()
