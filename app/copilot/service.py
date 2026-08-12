import uuid

from app.copilot.schemas import CopilotActionStep, CopilotRequest, CopilotResponse
from app.core.ai_gateway import global_ai_gateway
from app.core.memory import global_memory_service


class EnterpriseAICopilot:
    def __init__(self) -> None:
        self.gateway = global_ai_gateway
        self.memory = global_memory_service

    async def execute_copilot(self, user_id: uuid.UUID, workspace_id: uuid.UUID, request: CopilotRequest) -> CopilotResponse:
        session_id = request.session_id or f"copilot_sess_{uuid.uuid4().hex[:8]}"

        # Retrieve session context from Memory Service
        prev_chats = self.memory.session_memory.get(session_id, [])

        # Call AI Gateway to generate response
        ai_resp = await self.gateway.generate(
            prompt=f"User Request: {request.user_prompt}. Context Type: {request.context_type}",
            system_prompt="You are NexusBI Enterprise AI Copilot. Synthesize multi-step planning across data engineering, SQL, analytics, forecasting, dashboards, reports, and workflows.",
        )

        # Store in memory
        self.memory.record_chat(session_id, f"User: {request.user_prompt}\nCopilot: {ai_resp.text}")

        # Construct multi-step plan
        steps = [
            CopilotActionStep(
                step_number=1,
                action_type="recommend_cleaning",
                title="Data Health & Outlier Cleaning Recommendations",
                output_payload={"issues_detected": ["Missing email fields", "Outlier revenue values"], "recommendation": "Apply IQR clipping & median imputation"},
            ),
            CopilotActionStep(
                step_number=2,
                action_type="generate_sql",
                title="Generate Read-Only Aggregation SQL",
                output_payload={"sql": "SELECT category, SUM(revenue) AS total_revenue FROM SalesDataset GROUP BY category ORDER BY total_revenue DESC;"},
            ),
            CopilotActionStep(
                step_number=3,
                action_type="generate_dashboard",
                title="Generate Executive Dashboard Layout",
                output_payload={"widgets_count": 4, "layout": "grid_2x2", "chart_types": ["bar", "line", "kpi_card"]},
            ),
            CopilotActionStep(
                step_number=4,
                action_type="generate_report",
                title="Generate Executive Business Presentation",
                output_payload={"slides_count": 5, "format": "markdown_presentation", "summary": "Q2 Margin expansion presentation"},
            ),
        ]

        followups = [
            "Would you like to execute the generated workflow pipeline?",
            "Should I export the presentation as PDF?",
            "Do you want to set up an automated daily schedule?",
        ]

        return CopilotResponse(
            session_id=session_id,
            summary_insight=ai_resp.text or "Synthesized multi-step enterprise plan.",
            plan_steps=steps,
            suggested_followups=followups,
        )


global_copilot_service = EnterpriseAICopilot()
