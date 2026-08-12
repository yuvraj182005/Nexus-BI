from typing import Any

from pydantic import BaseModel, Field


class SQLGenerateRequest(BaseModel):
    prompt: str = Field(..., description="Natural language data query prompt")
    dialect: str = Field("duckdb", description="Target SQL dialect (duckdb, postgresql, mysql, sqlite)")


class SQLGenerateResponse(BaseModel):
    prompt: str
    generated_sql: str
    dialect: str
    confidence: float
    explanation: str
    semantic_mappings: dict[str, str]


class SQLExecuteRequest(BaseModel):
    sql: str = Field(..., description="SQL query string to execute")
    limit: int = Field(100, ge=1, le=1000)


class SQLExecuteResponse(BaseModel):
    sql: str
    execution_time_ms: float
    row_count: int
    columns: list[str]
    rows: list[dict[str, Any]]
    result_metadata: dict[str, Any]


class SQLExplainRequest(BaseModel):
    sql: str = Field(..., description="SQL query string to explain and optimize")


class SQLExplainResponse(BaseModel):
    sql: str
    explanation: str
    is_safe: bool
    estimated_cost: str
    join_recommendations: list[str]
    index_recommendations: list[str]
