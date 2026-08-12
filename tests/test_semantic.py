import pytest
from app.models.semantic import SemanticFieldRole, SemanticRelationshipType
from app.services.semantic import SemanticService


def test_infer_role_entity():
    role, confidence = SemanticService._infer_role("user_id", {})
    assert role == SemanticFieldRole.ENTITY
    assert confidence > 0.9


def test_infer_role_kpi():
    role, confidence = SemanticService._infer_role("total_revenue", {"numerical_summary": {}})
    assert role == SemanticFieldRole.KPI
    assert confidence >= 0.8


def test_relationship_mapping():
    assert SemanticService._relationship_type("primary_key") == SemanticRelationshipType.PRIMARY_KEY
    assert SemanticService._relationship_type("foreign_key") == SemanticRelationshipType.FOREIGN_KEY
    assert SemanticService._relationship_type("unknown") == SemanticRelationshipType.RELATED
