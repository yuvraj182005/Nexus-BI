from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    model_name: str = Field("mock-v1", description="Model name identifier")
    temperature: float = Field(0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(2048, ge=1, le=16384)
    timeout_seconds: float = Field(10.0, ge=0.1, le=120.0)
    input_cost_per_token: float = Field(0.0000015, ge=0.0)
    output_cost_per_token: float = Field(0.000002, ge=0.0)


class GatewayConfig(BaseModel):
    default_provider: str = Field("mock", description="Default active AI provider")
    fallback_chain: list[str] = Field(
        default_factory=lambda: ["openai", "anthropic", "gemini", "azure", "ollama", "mock"]
    )
    max_retries: int = Field(3, ge=0, le=10)
    rate_limit_per_minute: int = Field(600, ge=1)
