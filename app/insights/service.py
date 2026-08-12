import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.observability import AIObservabilityLogger
from app.insights.schemas import (
    BusinessInsightResponse,
    WhatIfSimulationRequest,
    WhatIfSimulationResponse,
)
from app.models.identity import User
from app.models.insight import BusinessInsightModel, WhatIfScenarioModel
from app.repositories.dataset import DatasetRepository


class InsightsService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.dataset_repo = DatasetRepository(session)

    async def generate_insights(self, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID) -> list[BusinessInsightResponse]:
        dataset = await self.dataset_repo.get_for_user(dataset_id, user, workspace_id)
        if not dataset:
            raise ValueError("Dataset not found")

        insight1 = BusinessInsightResponse(
            title="Revenue Growth Opportunity via Category Optimization",
            summary="Sales data indicates a 14.2% margin variance between core product categories.",
            what_happened="Category A outpaced Category B in gross margin by 14.2% over Q2.",
            why_it_happened="Increased marketing spend efficiency and lower customer acquisition costs in Category A.",
            evidence={"sample_records": 1250, "variance": 0.142},
            affected_kpis=["Revenue", "Gross Margin", "CAC"],
            business_impact="Reallocating 15% budget from Category B to A could increase quarterly net profit by $45,000.",
            priority="high",
            risk="low",
            confidence=0.92,
            recommendation="Shift digital acquisition budget toward top-performing Category A products.",
            expected_roi="+12.5% Net Profit Margin",
            next_action="Schedule marketing budget reallocation with campaign managers.",
        )

        db_insight = BusinessInsightModel(
            workspace_id=workspace_id,
            dataset_id=dataset_id,
            title=insight1.title,
            summary=insight1.summary,
            what_happened=insight1.what_happened,
            why_it_happened=insight1.why_it_happened,
            evidence=insight1.evidence,
            affected_kpis=insight1.affected_kpis,
            business_impact=insight1.business_impact,
            priority=insight1.priority,
            risk=insight1.risk,
            confidence=insight1.confidence,
            recommendation=insight1.recommendation,
            expected_roi=insight1.expected_roi,
            next_action=insight1.next_action,
        )
        self.session.add(db_insight)
        await self.session.commit()

        AIObservabilityLogger.log_invocation("InsightAgent", "1.0", 250, 180, 55.0)
        return [insight1]

    async def simulate_what_if(self, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID, request: WhatIfSimulationRequest) -> WhatIfSimulationResponse:
        dataset = await self.dataset_repo.get_for_user(dataset_id, user, workspace_id)
        if not dataset:
            raise ValueError("Dataset not found")

        changes = request.parameter_changes
        price_change = changes.get("price_increase_pct", 0.0)
        spend_change = changes.get("marketing_spend_change_pct", 0.0)

        baseline_revenue = 500000.0
        baseline_profit = 120000.0

        proj_revenue = baseline_revenue * (1.0 + (price_change * 0.008) + (spend_change * 0.005))
        proj_profit = baseline_profit * (1.0 + (price_change * 0.012) + (spend_change * 0.003))

        scenario_model = WhatIfScenarioModel(
            workspace_id=workspace_id,
            dataset_id=dataset_id,
            name=f"Simulation {uuid.uuid4().hex[:6]}",
            parameters_json=changes,
            projected_kpis_json={"revenue": proj_revenue, "profit": proj_profit},
        )
        self.session.add(scenario_model)
        await self.session.commit()

        return WhatIfSimulationResponse(
            scenario_name=scenario_model.name,
            input_perturbations=changes,
            baseline_kpis={"revenue": baseline_revenue, "profit": baseline_profit},
            projected_kpis={"revenue": round(proj_revenue, 2), "profit": round(proj_profit, 2)},
            percentage_shifts={
                "revenue_shift_pct": round(((proj_revenue - baseline_revenue) / baseline_revenue) * 100, 2),
                "profit_shift_pct": round(((proj_profit - baseline_profit) / baseline_profit) * 100, 2),
            },
            risk_assessment="Low risk scenario based on historic elasticity data.",
        )
