import re
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.models.dataset import Dataset, DatasetVersion
from app.models.identity import User
from app.models.profile import DatasetProfileReport, ProfileStatus
from app.models.semantic import (
    GlossaryTerm,
    SemanticField,
    SemanticFieldRole,
    SemanticLayer,
    SemanticRelationship,
    SemanticRelationshipType,
    SemanticStatus,
)
from app.repositories.semantic import SemanticRepository
from app.schemas.semantic import GlossaryTermCreateRequest, SemanticFieldUpdateRequest

BUSINESS_VOCABULARY: dict[str, tuple[str, list[str]]] = {
    "revenue": ("Revenue", ["sales", "income", "turnover", "amount"]),
    "profit": ("Profit", ["earnings", "net income", "margin"]),
    "cost": ("Cost", ["expense", "spend", "expenditure"]),
    "customer": ("Customer", ["client", "account", "buyer"]),
    "product": ("Product", ["item", "sku", "offering"]),
    "order": ("Order", ["transaction", "purchase"]),
    "inventory": ("Inventory", ["stock", "quantity on hand"]),
    "employee": ("Employee", ["staff", "worker", "headcount"]),
    "date": ("Date", ["time", "period", "month", "year"]),
}


class SemanticService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.repository = SemanticRepository(session)

    async def generate(self, version_id: uuid.UUID) -> SemanticLayer | None:
        version = await self.session.get(DatasetVersion, version_id)
        if not version:
            return None
        dataset = await self.session.get(Dataset, version.dataset_id)
        report = await self.session.scalar(
            select(DatasetProfileReport).where(DatasetProfileReport.dataset_version_id == version.id)
        )
        if not dataset or not report or report.status != ProfileStatus.READY:
            return None
        layer = await self.repository.get_layer(dataset.id, version.id)
        if layer is None:
            layer = SemanticLayer(dataset_id=dataset.id, dataset_version_id=version.id)
            self.session.add(layer)
            await self.session.flush()
        layer.status = SemanticStatus.PROCESSING
        await self.session.commit()
        try:
            glossary = await self.repository.list_glossary(dataset.workspace_id)
            fields = self._infer_fields(report.column_profiles or [], glossary)
            layer.business_domain = self._infer_domain(fields, dataset.name)
            layer.glossary_json = {
                "terms": {field["canonical_name"]: field["synonyms"] for field in fields},
                "domain": layer.business_domain,
            }
            existing_fields = await self.repository.get_fields(layer.id)
            for field in existing_fields:
                await self.session.delete(field)
            await self.session.flush()
            persisted: dict[str, SemanticField] = {}
            for field_data in fields:
                field = SemanticField(semantic_layer_id=layer.id, **field_data)
                self.session.add(field)
                persisted[field.source_column] = field
            await self.session.flush()
            existing_relationships = await self.repository.get_relationships(layer.id)
            for relationship in existing_relationships:
                await self.session.delete(relationship)
            for candidate in report.relationships or []:
                source = persisted.get(candidate.get("column"))
                if source:
                    self.session.add(
                        SemanticRelationship(
                            semantic_layer_id=layer.id,
                            source_field_id=source.id,
                            relationship_type=self._relationship_type(candidate.get("candidate")),
                            confidence=float(candidate.get("confidence", 0.5)),
                            metadata_json={"source": "profiling_report"},
                        )
                    )
            layer.status = SemanticStatus.READY
            layer.error_message = None
        except Exception as exc:
            layer.status = SemanticStatus.FAILED
            layer.error_message = str(exc)[:2000]
        await self.session.commit()
        return layer

    async def update_field(
        self, layer: SemanticLayer, source_column: str, request: SemanticFieldUpdateRequest
    ) -> SemanticField:
        field = await self.session.scalar(
            select(SemanticField).where(
                SemanticField.semantic_layer_id == layer.id,
                SemanticField.source_column == source_column,
            )
        )
        if not field:
            raise ValueError("Semantic field not found")
        changes = request.model_dump(exclude_unset=True)
        for key, value in changes.items():
            setattr(field, key, value)
        field.is_user_defined = True
        await self.session.commit()
        return field

    async def create_glossary_term(
        self, user: User, workspace_id: uuid.UUID, request: GlossaryTermCreateRequest
    ) -> GlossaryTerm:
        existing = await self.session.scalar(
            select(GlossaryTerm).where(
                GlossaryTerm.workspace_id == workspace_id,
                GlossaryTerm.term == request.term,
            )
        )
        if existing:
            raise ValueError("Glossary term already exists in this workspace")
        term = GlossaryTerm(
            organization_id=user.organization_id,
            workspace_id=workspace_id,
            owner_id=user.id,
            term=request.term,
            definition=request.definition,
            synonyms=request.synonyms,
            example_values=request.example_values,
        )
        self.session.add(term)
        await self.session.commit()
        return term

    @classmethod
    def _infer_fields(cls, profiles: list[dict], glossary: list[GlossaryTerm]) -> list[dict[str, Any]]:
        fields = []
        for profile in profiles:
            source = str(profile.get("name", "column"))
            normalized = cls._normalize(source)
            role, confidence = cls._infer_role(source, profile)
            canonical, display, synonyms = cls._canonical(source, normalized, glossary)
            fields.append(
                {
                    "source_column": source,
                    "canonical_name": canonical,
                    "display_name": display,
                    "role": role,
                    "data_type": str(profile.get("data_type", "unknown")),
                    "description": cls._description(display, role, profile),
                    "expression": None,
                    "synonyms": synonyms,
                    "confidence": confidence,
                    "is_user_defined": False,
                }
            )
        return fields

    @classmethod
    def _infer_role(cls, source: str, profile: dict) -> tuple[str, float]:
        normalized = cls._normalize(source)
        if normalized == "id" or normalized.endswith("_id"):
            return SemanticFieldRole.ENTITY, 0.96
        if "date_summary" in profile or any(token in normalized for token in ("date", "time", "month", "year")):
            return SemanticFieldRole.DATE, 0.9
        if "numerical_summary" in profile:
            for token in ("revenue", "sales", "profit", "cost", "amount", "price", "quantity", "rate", "score"):
                if token in normalized:
                    return SemanticFieldRole.KPI, 0.9
            return SemanticFieldRole.MEASURE, 0.82
        if "categorical_summary" in profile:
            return SemanticFieldRole.DIMENSION, 0.84
        return SemanticFieldRole.ATTRIBUTE, 0.55

    @classmethod
    def _canonical(cls, source: str, normalized: str, glossary: list[GlossaryTerm]):
        for term in glossary:
            vocabulary = [term.term, *(term.synonyms or [])]
            if any(cls._normalize(value) in normalized or normalized in cls._normalize(value) for value in vocabulary):
                return cls._normalize(term.term), term.term, vocabulary
        for canonical, (display, synonyms) in BUSINESS_VOCABULARY.items():
            if canonical in normalized or any(alias.replace(" ", "_") in normalized for alias in synonyms):
                return canonical, display, [canonical, *synonyms]
        return normalized, source.replace("_", " ").title(), [normalized]

    @staticmethod
    def _description(display: str, role: str, profile: dict) -> str:
        count = profile.get("unique_count")
        suffix = f" with {count} distinct values" if count is not None else ""
        return f"{display} semantic {role} inferred from the source column{suffix}."

    @staticmethod
    def _infer_domain(fields: list[dict], dataset_name: str) -> str:
        text = " ".join([dataset_name, *(field["canonical_name"] for field in fields)]).lower()
        domains = {
            "sales": ("revenue", "sales", "order", "product"),
            "finance": ("profit", "cost", "expense", "budget"),
            "hr": ("employee", "salary", "headcount"),
            "marketing": ("campaign", "conversion", "lead"),
            "inventory": ("inventory", "stock", "warehouse"),
        }
        return max(domains, key=lambda domain: sum(token in text for token in domains[domain]))

    @staticmethod
    def _relationship_type(value: str | None) -> str:
        mapping = {
            "primary_key": SemanticRelationshipType.PRIMARY_KEY,
            "foreign_key": SemanticRelationshipType.FOREIGN_KEY,
        }
        return mapping.get(value or "", SemanticRelationshipType.RELATED)

    @staticmethod
    def _normalize(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
