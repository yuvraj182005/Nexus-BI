import uuid
from typing import Any

from pydantic import BaseModel, Field


class GovernancePolicyRequest(BaseModel):
    sensitivity_label: str = Field("Internal", description="Public, Internal, Confidential, Restricted")
    retention_days: int = Field(365, ge=1)
    business_owner: str = Field("Data Governance Board")
    compliance_rules: list[str] = Field(default_factory=lambda: ["GDPR", "HIPAA", "SOC2"])
    masking_rules: dict[str, str] = Field(default_factory=dict, description="e.g. {'email': 'mask_domain'}")


class PIIScanResponse(BaseModel):
    dataset_id: uuid.UUID
    pii_detected_columns: dict[str, list[str]]
    recommended_sensitivity: str
    column_masking_status: dict[str, str]


class GovernanceAuditResponse(BaseModel):
    dataset_id: uuid.UUID
    sensitivity_label: str
    is_certified: bool
    retention_days: int
    business_owner: str
    compliance_status: str
    data_quality_monitoring: dict[str, Any]
    column_security_policies: list[dict[str, Any]]
