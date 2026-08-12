# 🚀 NexusBI AI

> Enterprise AI-Powered Business Intelligence & Decision Intelligence Platform

NexusBI AI is a modern enterprise platform that combines **Business Intelligence, Artificial Intelligence, Data Analytics, Machine Learning, SQL Intelligence, Forecasting, Workflow Automation, and Interactive Dashboards** into a single unified system.

It enables organizations to transform raw business data into actionable insights through AI-powered analytics, automated workflows, natural language querying, and real-time visualizations.

---

## ✨ Key Features

- 🔐 Enterprise Authentication & RBAC
- 📂 Workspace & Dataset Management
- 🔌 Multiple Data Connectors
- 📊 Automated Data Profiling
- 🧹 AI Data Cleaning & Transformation
- 🏷️ Semantic Layer & Business Glossary
- 🤖 Natural Language to SQL
- 📈 Analytics & Forecasting
- 💡 AI Business Insights
- 📉 Interactive Dashboards
- 💬 Chat with Data (Hybrid RAG)
- 🤝 Collaboration Workspace
- 🔄 Workflow Automation
- 📦 Plugin Marketplace
- 🛡️ Governance & Audit Logs
- 📡 Real-Time Streaming Analytics
- 📑 Report Generation
- 📊 Enterprise Observability
- 💳 SaaS Billing & Subscription Management

---

## 🏗️ Architecture

```
Frontend (Next.js + React)
          │
          ▼
FastAPI REST API
          │
────────────────────────────────────────
AI Gateway
Hybrid RAG
Workflow Engine
Job Orchestrator
Streaming Engine
Security Layer
Analytics Engine
Forecast Engine
SQL Intelligence
Visualization Engine
────────────────────────────────────────
          │
 PostgreSQL | MongoDB | Redis | DuckDB
```

---

## 🛠️ Tech Stack

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Framer Motion
- GSAP
- ECharts
- Plotly

### Backend
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- MongoDB
- Redis
- DuckDB
- Celery

### AI & Analytics
- OpenAI
- Anthropic Claude
- Gemini
- Ollama
- Hybrid RAG
- LangChain
- Scikit-Learn
- Pandas
- NumPy

### DevOps
- Docker
- GitHub Actions
- Prometheus
- OpenTelemetry

---

## 📂 Project Structure

```
frontend/
backend/

backend/app/
 ├── analytics
 ├── audit
 ├── auth
 ├── catalog
 ├── collaboration
 ├── connectors
 ├── copilot
 ├── dashboards
 ├── datasets
 ├── forecasting
 ├── governance
 ├── insights
 ├── jobs
 ├── lineage
 ├── marketplace
 ├── observability
 ├── plugins
 ├── preprocessing
 ├── rag
 ├── reports
 ├── saas
 ├── search
 ├── security
 ├── semantic
 ├── sql_engine
 ├── streaming
 ├── visualization
 └── workflows
```

---

## 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/yourusername/NexusBI-AI.git
cd NexusBI-AI
```

### Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## 🌐 API Documentation

```
http://localhost:8000/api/v1/docs
```

---

## 📊 Core Workflow

```
Login
   ↓
Workspace
   ↓
Upload Dataset
   ↓
Data Profiling
   ↓
AI Cleaning
   ↓
Semantic Layer
   ↓
Natural Language SQL
   ↓
Analytics
   ↓
Forecasting
   ↓
Visualization
   ↓
Dashboard Builder
   ↓
Reports
```

---

## 🔒 Enterprise Features

- Multi-Tenant Architecture
- JWT Authentication
- RBAC
- MFA Support
- Hybrid RAG
- AI Gateway
- Audit Logs
- Governance
- Plugin SDK
- Workflow Automation
- Streaming Analytics
- Observability

---

                    ┌──────────────────────┐
                    │     NexusBI AI       │
                    │ Decision Intelligence│
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   Data Layer              AI Layer             Experience
        │                      │                      │
 ┌──────┴──────┐        ┌──────┴──────┐        ┌──────┴──────┐
 │ Connectors  │        │ AI Gateway  │        │ Dashboards  │
 │ Datasets    │        │ AI Agents   │        │ Analytics   │
 │ PostgreSQL  │        │ RAG         │        │ Reports     │
 │ MongoDB     │        │ Copilot     │        │ Chat        │
 │ Files       │        │ Memory      │        │ Visuals     │
 └─────────────┘        └─────────────┘        └─────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                  ┌────────────┴────────────┐
                  │ Governance & Security   │
                  │ RBAC • Audit • Lineage  │
                  │ PII • Compliance        │
                  └─────────────────────────┘



## 👨‍💻 Author

**K. Yuvraj Sundaram**

- LinkedIn: https://linkedin.com/in/k-yuvraj-sundaram-a34790352

---

⭐ If you find this project useful, consider giving it a star.
