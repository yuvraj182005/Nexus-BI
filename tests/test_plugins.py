import pytest
from app.plugins.registry import global_plugin_registry
from app.plugins.schemas import PluginManifest, PluginRegisterRequest


def test_plugin_registration_and_validation():
    manifest = PluginManifest(
        plugin_id="partner_forecast_v1",
        name="Partner DeepAR Forecaster",
        plugin_type="forecast",
        author="Partner Team",
    )
    req = PluginRegisterRequest(manifest=manifest, code="class Handler: pass")
    registered = global_plugin_registry.register_plugin(req)
    assert registered.plugin_id == "partner_forecast_v1"
    assert global_plugin_registry.get_plugin("partner_forecast_v1") is not None


def test_plugin_invalid_type():
    manifest = PluginManifest(
        plugin_id="bad_plugin",
        name="Bad Type",
        plugin_type="invalid_type",
        author="Test",
    )
    req = PluginRegisterRequest(manifest=manifest, code="")
    with pytest.raises(ValueError, match="Invalid plugin type"):
        global_plugin_registry.register_plugin(req)
