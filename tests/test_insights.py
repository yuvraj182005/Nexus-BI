import pytest
from app.insights.schemas import WhatIfSimulationRequest


def test_what_if_request_schema():
    req = WhatIfSimulationRequest(parameter_changes={"price_increase_pct": 5.0})
    assert req.parameter_changes["price_increase_pct"] == 5.0
