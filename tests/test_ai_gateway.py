import pytest
from app.core.ai_gateway import (
    AIGateway,
    AnthropicProvider,
    AzureOpenAIProvider,
    GeminiProvider,
    MockProvider,
    OllamaProvider,
    OpenAIProvider,
    ProviderRouter,
)


@pytest.mark.asyncio
async def test_provider_instantiation():
    router = ProviderRouter()
    assert isinstance(router.get_provider("openai"), OpenAIProvider)
    assert isinstance(router.get_provider("anthropic"), AnthropicProvider)
    assert isinstance(router.get_provider("gemini"), GeminiProvider)
    assert isinstance(router.get_provider("azure"), AzureOpenAIProvider)
    assert isinstance(router.get_provider("ollama"), OllamaProvider)
    assert isinstance(router.get_provider("mock"), MockProvider)


@pytest.mark.asyncio
async def test_ai_gateway_generate_text():
    gateway = AIGateway()
    res = await gateway.generate_text("Summarize quarterly revenue", preferred_provider="openai")
    assert "Response to: Summarize quarterly revenue" in res


@pytest.mark.asyncio
async def test_ai_gateway_fallback_chain():
    gateway = AIGateway()
    # Mark OpenAI unhealthy
    openai_p = gateway.router.get_provider("openai")
    assert openai_p is not None
    openai_p.mark_unhealthy()

    # Request preferred OpenAI -> should fall back to next healthy provider in chain
    res = await gateway.generate_text("Analyze churn rate", preferred_provider="openai")
    assert "Response to: Analyze churn rate" in res


@pytest.mark.asyncio
async def test_ai_gateway_json_generation():
    gateway = AIGateway()
    data = await gateway.generate_json("Generate insights schema", preferred_provider="gemini")
    assert "provider" in data
    assert "model" in data
