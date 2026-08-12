from typing import Any

PROMPT_TEMPLATES: dict[str, str] = {
    "sql_generate": "Generate a read-only SQL query for dataset '{dataset_name}' to answer: {question}. Use dialect {dialect}.",
    "sql_explain": "Explain the following SQL query in simple business terms: {sql}",
    "insight_generate": "Analyze dataset metrics and generate executive business insights.",
    "forecast_predict": "Generate time series forecasting using model {model_name} for period length {steps}.",
    "chart_recommend": "Recommend visual chart specifications for data profile: {profile_summary}.",
}


class PromptManager:
    @staticmethod
    def render(template_key: str, **kwargs: Any) -> str:
        template = PROMPT_TEMPLATES.get(template_key, "{question}")
        try:
            return template.format(**kwargs)
        except Exception:
            return template
