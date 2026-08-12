# NexusBI AI Plugin SDK Developer Guide

NexusBI AI supports extensible external plugins across 7 plugin types:

1. **Connector**: Custom database or SaaS connectors.
2. **Visualization**: Custom chart renderers or Plotly/D3 wrappers.
3. **Forecast**: Custom time-series models (e.g. ARIMA, DeepAR).
4. **Analytics**: Custom statistical tests or domain models.
5. **AI**: Custom LLM provider adapters.
6. **Notification**: Custom alert dispatchers (PagerDuty, Teams, Webhook).
7. **Workflow**: Custom DAG workflow steps.

---

## 1. Plugin Manifest Structure

Every plugin must define a `manifest` specification:

```json
{
  "plugin_id": "custom_custom_connector_v1",
  "name": "Custom SaaS Connector",
  "version": "1.0.0",
  "plugin_type": "connector",
  "author": "Partner Dev Team",
  "permissions": ["read_dataset", "execute_query"],
  "config_schema": {
    "api_key": "string",
    "endpoint_url": "string"
  },
  "entry_point": "handler:CustomPluginHandler",
  "is_active": true
}
```

---

## 2. Implementation Example

```python
class CustomPluginHandler:
    def __init__(self, config: dict):
        self.config = config

    def execute(self, payload: dict) -> dict:
        return {"status": "success", "result": "Plugin processed data"}
```

---

## 3. Hot Reloading Plugins

Plugins can be hot-reloaded dynamically without restarting the API process by triggering `global_plugin_registry.hot_reload()`.
