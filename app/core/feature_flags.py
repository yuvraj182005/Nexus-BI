FEATURE_FLAGS = {
    "sql_ai_engine": True,
    "analytics_engine": True,
    "forecasting_engine": True,
    "insights_engine": True,
    "visualization_engine": True,
    "multi_agent_system": True,
    "chat_rag_engine": True,
    "reports_notifications": True,
}


def is_feature_enabled(flag: str) -> bool:
    return FEATURE_FLAGS.get(flag, True)
