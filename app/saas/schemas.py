import uuid

from pydantic import BaseModel, Field


class SubscriptionPlan(BaseModel):
    plan_name: str = Field(..., description="Free, Pro, Enterprise")
    monthly_price_usd: float
    max_datasets: int
    max_storage_mb: float
    max_api_calls_per_day: int
    feature_flags: list[str]


class WorkspaceUsageDashboard(BaseModel):
    workspace_id: uuid.UUID
    current_plan: str
    datasets_count: int
    datasets_limit: int
    storage_used_mb: float
    storage_limit_mb: float
    api_calls_today: int
    api_calls_limit: int
    billing_status: str  # active, past_due, trialing, canceled
    next_billing_date: float


class InvoiceRecord(BaseModel):
    invoice_id: str
    workspace_id: uuid.UUID
    amount_usd: float
    status: str  # paid, pending, failed
    billing_period: str
    pdf_download_url: str
