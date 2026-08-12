from typing import Any

from pydantic import BaseModel, Field


class BusinessInsightResponse(BaseModel):
    title: str
    summary: str
    what_happened: str
    why_it_happened: str
    evidence: dict[str, Any]
    affected_kpis: list[str]
    business_impact: str
    priority: str
    risk: str
    confidence: float
    recommendation: str
    expected_roi: str
    next_action: str


class WhatIfSimulationRequest(BaseModel):
    parameter_changes: dict[str, float] = Field(..., description="Perturbations, e.g. {'price_increase_pct': 5.0, 'marketing_spend_change_pct': 10.0}")


class WhatIfSimulationResponse(BaseModel):
    scenario_name: str
    input_perturbations: dict[str, float]
    baseline_kpis: dict[str, float]
    projected_kpis: dict[str, float]
    percentage_shifts: dict[str, float]
    risk_assessment: str
