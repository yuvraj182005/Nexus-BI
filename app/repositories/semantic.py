import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.semantic import GlossaryTerm, SemanticField, SemanticLayer, SemanticRelationship


class SemanticRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_layer(self, dataset_id: uuid.UUID, version_id: uuid.UUID | None = None) -> SemanticLayer | None:
        statement = select(SemanticLayer).where(SemanticLayer.dataset_id == dataset_id)
        if version_id:
            statement = statement.where(SemanticLayer.dataset_version_id == version_id)
        else:
            statement = statement.order_by(SemanticLayer.created_at.desc())
        return await self.session.scalar(statement)

    async def get_fields(self, layer_id: uuid.UUID) -> list[SemanticField]:
        return list((await self.session.scalars(select(SemanticField).where(SemanticField.semantic_layer_id == layer_id))).all())

    async def get_relationships(self, layer_id: uuid.UUID) -> list[SemanticRelationship]:
        return list((await self.session.scalars(select(SemanticRelationship).where(SemanticRelationship.semantic_layer_id == layer_id))).all())

    async def list_glossary(self, workspace_id: uuid.UUID) -> list[GlossaryTerm]:
        statement = select(GlossaryTerm).where(GlossaryTerm.workspace_id == workspace_id).order_by(GlossaryTerm.term)
        return list((await self.session.scalars(statement)).all())
