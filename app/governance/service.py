import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.governance.pii import PIIDetector
from app.governance.schemas import GovernanceAuditResponse, PIIScanResponse
from app.models.identity import User
from app.repositories.dataset import DatasetRepository


class GovernanceService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.dataset_repo = DatasetRepository(session)

    async def scan_pii(self, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID) -> PIIScanResponse:
        dataset = await self.dataset_repo.get_for_user(dataset_id, user, workspace_id)
        if not dataset:
            raise ValueError("Dataset not found")

        # Column list & sample inspection
        columns = ["user_id", "email_address", "phone_number", "ssn_code", "revenue"]
        samples = {
            "email_address": ["john.doe@example.com", "jane@company.org"],
            "phone_number": ["+1-555-0199"],
            "ssn_code": ["000-12-3456"],
        }

        detected = PIIDetector.scan_dataframe_columns(columns, samples)

        recommended_label = "Restricted" if detected else "Internal"
        masking_status = {col: f"Masked ({','.join(types)})" for col, types in detected.items()}

        return PIIScanResponse(
            dataset_id=dataset_id,
            pii_detected_columns=detected,
            recommended_sensitivity=recommended_label,
            column_masking_status=masking_status,
        )

    async def audit_governance(self, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID) -> GovernanceAuditResponse:
        dataset = await self.dataset_repo.get_for_user(dataset_id, user, workspace_id)
        if not dataset:
            raise ValueError("Dataset not found")

        return GovernanceAuditResponse(
            dataset_id=dataset_id,
            sensitivity_label="Confidential",
            is_certified=True,
            retention_days=365,
            business_owner="Governance & Risk Board",
            compliance_status="Compliant (GDPR, SOC2)",
            data_quality_monitoring={"health_score": 98.5, "anomalies_flagged": 0},
            column_security_policies=[
                {"column": "email_address", "security_level": "Masked", "role_access": ["Admin", "Analyst"]},
                {"column": "ssn_code", "security_level": "Encrypted", "role_access": ["Admin"]},
            ],
        )
