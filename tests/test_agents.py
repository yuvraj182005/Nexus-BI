import pytest
from app.agents.orchestrator import AgentOrchestrator


def test_agent_list():
    assert len(AgentOrchestrator.ALL_AGENTS) == 8
    assert "SQL Agent" in AgentOrchestrator.ALL_AGENTS
    assert "Data Engineer Agent" in AgentOrchestrator.ALL_AGENTS
