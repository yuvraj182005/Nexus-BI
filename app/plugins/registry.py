import time

from app.plugins.schemas import PluginManifest, PluginRegisterRequest


class PluginRegistry:
    VALID_TYPES = {"connector", "visualization", "forecast", "analytics", "ai", "notification", "workflow"}

    def __init__(self) -> None:
        self._plugins: dict[str, PluginManifest] = {}
        self._code_store: dict[str, str] = {}
        self._last_reload_timestamp: float = time.time()

    def validate_manifest(self, manifest: PluginManifest) -> tuple[bool, str | None]:
        if manifest.plugin_type not in self.VALID_TYPES:
            return False, f"Invalid plugin type '{manifest.plugin_type}'. Must be one of {self.VALID_TYPES}"
        if not manifest.plugin_id or not manifest.name:
            return False, "Plugin ID and Name are required."
        return True, None

    def register_plugin(self, request: PluginRegisterRequest) -> PluginManifest:
        valid, error = self.validate_manifest(request.manifest)
        if not valid:
            raise ValueError(error or "Manifest validation failed")

        self._plugins[request.manifest.plugin_id] = request.manifest
        self._code_store[request.manifest.plugin_id] = request.code
        return request.manifest

    def hot_reload(self) -> int:
        self._last_reload_timestamp = time.time()
        # Simulated dynamic module re-import / cache flush
        return len(self._plugins)

    def get_plugin(self, plugin_id: str) -> PluginManifest | None:
        return self._plugins.get(plugin_id)

    def list_plugins(self, plugin_type: str | None = None) -> list[PluginManifest]:
        plugins = list(self._plugins.values())
        if plugin_type:
            plugins = [p for p in plugins if p.plugin_type == plugin_type]
        return plugins


global_plugin_registry = PluginRegistry()
