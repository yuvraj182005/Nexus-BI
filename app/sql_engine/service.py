import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.observability import AIObservabilityLogger
from app.models.identity import User
from app.models.sql import SQLExecutionHistory
from app.repositories.dataset import DatasetRepository
from app.repositories.semantic import SemanticRepository
from app.services.storage import StorageService
from app.sql_engine.engine import SQLAIEngine
from app.sql_engine.executor import SQLExecutor
from app.sql_engine.optimizer import SQLOptimizer
from app.sql_engine.schemas import (
    SQLExecuteRequest,
    SQLExecuteResponse,
    SQLExplainRequest,
    SQLExplainResponse,
    SQLGenerateRequest,
    SQLGenerateResponse,
)
from app.sql_engine.validators import SQLValidator


class SQLService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.dataset_repo = DatasetRepository(session)
        self.semantic_repo = SemanticRepository(session)

    async def generate_sql(self, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID, request: SQLGenerateRequest) -> SQLGenerateResponse:
        dataset = await self.dataset_repo.get_for_user(dataset_id, user, workspace_id)
        if not dataset:
            raise ValueError("Dataset not found")
        layer = await self.semantic_repo.get_layer(dataset.id)
        fields = await self.semantic_repo.get_fields(layer.id) if layer else []

        table_name = dataset.slug.replace("-", "_")
        sql, explanation, mappings = SQLAIEngine.generate_sql(request.prompt, table_name, fields, dialect=request.dialect)

        history = SQLExecutionHistory(
            workspace_id=workspace_id,
            dataset_id=dataset_id,
            user_id=user.id,
            prompt=request.prompt,
            generated_sql=sql,
            dialect=request.dialect,
            confidence=0.95,
            explanation=explanation,
        )
        self.session.add(history)
        await self.session.commit()

        AIObservabilityLogger.log_invocation("SQLAgent", "1.0", 120, 80, 45.0)

        return SQLGenerateResponse(
            prompt=request.prompt,
            generated_sql=sql,
            dialect=request.dialect,
            confidence=0.95,
            explanation=explanation,
            semantic_mappings=mappings,
        )

    async def execute_sql(self, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID, request: SQLExecuteRequest) -> SQLExecuteResponse:
        is_safe, error_msg = SQLValidator.validate_read_only(request.sql)
        if not is_safe:
            raise ValueError(error_msg or "SQL Query validation failed")

        dataset = await self.dataset_repo.get_for_user(dataset_id, user, workspace_id)
        if not dataset or not dataset.current_version_id:
            raise ValueError("Dataset or active version not found")

        version = await self.dataset_repo.get_version(dataset, dataset.current_version_id)
        if not version:
            raise ValueError("Dataset version not found")

        key = getattr(version, "storage_key", None) or getattr(version, "storage_path", None) or ""
        fmt = getattr(version, "format", None) or getattr(version, "file_format", None) or "csv"
        df = await StorageService(self.settings).read_dataframe(key, fmt)
        table_name = dataset.slug.replace("-", "_")

        columns, rows, elapsed_ms = SQLExecutor.execute_on_dataframe(df, table_name, request.sql, limit=request.limit)

        return SQLExecuteResponse(
            sql=request.sql,
            execution_time_ms=elapsed_ms,
            row_count=len(rows),
            columns=columns,
            rows=rows,
            result_metadata={"engine": "duckdb", "workspace_id": str(workspace_id)},
        )

    async def explain_sql(self, request: SQLExplainRequest) -> SQLExplainResponse:
        is_safe, _ = SQLValidator.validate_read_only(request.sql)
        analysis = SQLOptimizer.analyze(request.sql)
        return SQLExplainResponse(
            sql=request.sql,
            explanation=f"Query structure: SELECT block with filters. Execution safety: {'Safe' if is_safe else 'Unsafe'}.",
            is_safe=is_safe,
            estimated_cost=analysis["estimated_cost"],
            join_recommendations=analysis["join_recommendations"],
            index_recommendations=analysis["index_recommendations"],
        )
