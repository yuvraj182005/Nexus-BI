import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.schemas import EDARequest, EDAResponse
from app.core.config import Settings
from app.core.observability import AIObservabilityLogger
from app.models.identity import User
from app.repositories.dataset import DatasetRepository
from app.services.storage import StorageService


class AnalyticsService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.dataset_repo = DatasetRepository(session)

    async def run_eda(self, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID, request: EDARequest) -> EDAResponse:
        dataset = await self.dataset_repo.get_for_user(dataset_id, user, workspace_id)
        if not dataset or not dataset.current_version_id:
            raise ValueError("Dataset or active version not found")

        version = await self.dataset_repo.get_version(dataset, dataset.current_version_id)
        if not version:
            raise ValueError("Storage file version not found")

        key = getattr(version, "storage_key", None) or getattr(version, "storage_path", None) or ""
        fmt = getattr(version, "format", None) or getattr(version, "file_format", None) or "csv"
        df = await StorageService(self.settings).read_dataframe(key, fmt)

        domain = self._detect_domain(list(df.columns))
        stats = df.describe(include="all").to_dict()

        numeric_df = df.select_dtypes(include=["number"])
        corr = numeric_df.corr().fillna(0.0).to_dict() if not numeric_df.empty else {}

        outliers = {}
        for col in numeric_df.columns:
            q1 = numeric_df[col].quantile(0.25)
            q3 = numeric_df[col].quantile(0.75)
            iqr = q3 - q1
            cnt = int(((numeric_df[col] < (q1 - 1.5 * iqr)) | (numeric_df[col] > (q3 + 1.5 * iqr))).sum())
            outliers[col] = cnt

        AIObservabilityLogger.log_invocation("AnalyticsAgent", "1.0", 200, 150, 60.0)

        return EDAResponse(
            detected_domain=domain,
            row_count=len(df),
            column_count=len(df.columns),
            descriptive_stats=stats,
            correlation_matrix=corr,
            outlier_summary=outliers,
            insights_summary=[
                f"Dataset represents domain: {domain}.",
                f"Contains {len(df)} records across {len(df.columns)} feature attributes.",
            ],
        )

    @staticmethod
    def _detect_domain(columns: list[str]) -> str:
        cols_text = " ".join(columns).lower()
        if any(term in cols_text for term in ["revenue", "sales", "price", "order"]):
            return "Sales"
        if any(term in cols_text for term in ["employee", "salary", "headcount"]):
            return "HR"
        if any(term in cols_text for term in ["cost", "budget", "expense"]):
            return "Finance"
        if any(term in cols_text for term in ["campaign", "lead", "conversion"]):
            return "Marketing"
        return "General Business"
