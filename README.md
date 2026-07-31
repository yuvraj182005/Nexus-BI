# NexusBI AI

NexusBI AI is a multi-tenant FastAPI backend for enterprise decision intelligence. The codebase is organized by ownership boundaries: HTTP APIs, application services, repositories, domain engines, asynchronous tasks, AI Gateway, AI Memory, Workflow Automation, Job Orchestration, Data Catalog, Governance Center, Audit Center, Plugin SDK, Observability Center, Enterprise Identity Management, Collaboration Engine, Streaming Analytics, Enterprise AI Copilot, Dashboard Builder Engine, Lineage & Impact Analysis, Global Enterprise Search, Security Hardening Service, SaaS Platform Billing Engine, Plugin & Template Marketplace, Performance Optimizer, and infrastructure adapters.

## Local deployment

1. Install Python 3.13+ and Docker Desktop.
2. Copy `.env.example` to `.env` and replace `SECRET_KEY` with a random secret.
3. Start infrastructure and the API:

```powershell
docker compose up --build
```

4. Run database migrations:
```powershell
alembic upgrade head
```

5. Open the generated OpenAPI document at `http://localhost:8000/api/v1/docs`.

---

## Security Hardening (`app/security`)

- Security report available in [SECURITY_REPORT.md](file:///C:/Users/K%20BHRAMEE%20SUNDARAM/.gemini/antigravity/brain/73c29603-1059-4888-b22e-79cdec9746ab/SECURITY_REPORT.md).
- **Prompt Injection & RAG Guardrails**: Scans for system prompt overrides, jailbreaks, and injection payloads.
- **XSS & SQL Injection Protection**: DuckDB AST validator blocking mutating keywords (`DROP`, `DELETE`, `TRUNCATE`, `EXEC`) and XSS string sanitizer.
- **File Upload Validation**: Extension restriction and binary header malware detection (`MZ`, `ELF`).

---

## SaaS Multi-Tenant Billing Engine (`app/saas`)

- **Subscription Plans**: `Free`, `Pro`, `Enterprise` tier limits.
- **Usage Tracking**: Datasets limit, storage MB limit, and daily API calls limits.
- **Invoicing & Webhooks**: Stripe webhook simulator and PDF invoice downloading.

---

## Plugin & Template Marketplace (`app/marketplace`)

- **Marketplace Categories**: Plugins, Connectors, Dashboard Templates, Workflow Templates, AI Prompts, Report Templates, Visualization Templates.
- **Capabilities**: Ratings, reviews, version management, and one-click installation.

---

## Complete API Surface

### SaaS Billing API
```text
GET  /api/v1/workspaces/{workspace_id}/saas/usage
POST /api/v1/workspaces/{workspace_id}/saas/payment-webhook
```

### Marketplace API
```text
GET  /api/v1/workspaces/{workspace_id}/marketplace/items
POST /api/v1/workspaces/{workspace_id}/marketplace/items/{item_id}/install
POST /api/v1/workspaces/{workspace_id}/marketplace/items/{item_id}/review
```

### Enterprise Data Lineage & Impact Analysis
```text
GET /api/v1/workspaces/{workspace_id}/datasets/{dataset_id}/lineage-graph
GET /api/v1/workspaces/{workspace_id}/lineage/impact-analysis
```

### Global Enterprise Search API
```text
POST /api/v1/workspaces/{workspace_id}/search
POST /api/v1/workspaces/{workspace_id}/search/saved
GET  /api/v1/workspaces/{workspace_id}/search/history
```

### Enterprise AI Copilot API
```text
POST /api/v1/workspaces/{workspace_id}/copilot/execute
```

### Dashboard Builder API
```text
POST /api/v1/workspaces/{workspace_id}/dashboards/builder
POST /api/v1/workspaces/{workspace_id}/dashboards/{dashboard_id}/snapshot
POST /api/v1/workspaces/{workspace_id}/dashboards/{dashboard_id}/bookmarks
```
