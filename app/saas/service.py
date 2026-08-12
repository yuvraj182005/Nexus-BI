import time
import uuid

from app.saas.schemas import InvoiceRecord, SubscriptionPlan, WorkspaceUsageDashboard


class SaaSBillingService:
    PLANS = {
        "Free": SubscriptionPlan(
            plan_name="Free",
            monthly_price_usd=0.0,
            max_datasets=5,
            max_storage_mb=500.0,
            max_api_calls_per_day=1000,
            feature_flags=["profiling", "sql_engine"],
        ),
        "Pro": SubscriptionPlan(
            plan_name="Pro",
            monthly_price_usd=49.0,
            max_datasets=50,
            max_storage_mb=10000.0,
            max_api_calls_per_day=50000,
            feature_flags=["profiling", "sql_engine", "forecasting", "dashboards", "rag"],
        ),
        "Enterprise": SubscriptionPlan(
            plan_name="Enterprise",
            monthly_price_usd=499.0,
            max_datasets=1000,
            max_storage_mb=1000000.0,
            max_api_calls_per_day=1000000,
            feature_flags=["all"],
        ),
    }

    def __init__(self) -> None:
        self._subscriptions: dict[str, str] = {}  # workspace_id -> plan_name
        self._invoices: list[InvoiceRecord] = []

    def get_workspace_usage(self, workspace_id: uuid.UUID) -> WorkspaceUsageDashboard:
        ws_id = str(workspace_id)
        plan_name = self._subscriptions.get(ws_id, "Pro")
        plan = self.PLANS[plan_name]

        return WorkspaceUsageDashboard(
            workspace_id=workspace_id,
            current_plan=plan.plan_name,
            datasets_count=3,
            datasets_limit=plan.max_datasets,
            storage_used_mb=120.5,
            storage_limit_mb=plan.max_storage_mb,
            api_calls_today=1420,
            api_calls_limit=plan.max_api_calls_per_day,
            billing_status="active",
            next_billing_date=time.time() + (30 * 86400),
        )

    def process_payment_webhook(self, workspace_id: uuid.UUID, event_type: str, amount_usd: float) -> InvoiceRecord:
        inv = InvoiceRecord(
            invoice_id=f"inv_{uuid.uuid4().hex[:8]}",
            workspace_id=workspace_id,
            amount_usd=amount_usd,
            status="paid" if event_type == "payment_intent.succeeded" else "failed",
            billing_period="July 2026",
            pdf_download_url=f"/invoices/download/inv_{uuid.uuid4().hex[:8]}.pdf",
        )
        self._invoices.append(inv)
        return inv


global_saas_service = SaaSBillingService()
