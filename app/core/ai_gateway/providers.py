import abc
from typing import Any

from app.core.ai_gateway.config import ModelConfig


class BaseProvider(abc.ABC):
    def __init__(self, name: str, config: ModelConfig | None = None) -> None:
        self.name = name
        self.config = config or ModelConfig()
        self._is_healthy = True

    @abc.abstractmethod
    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> str:
        pass

    @abc.abstractmethod
    async def generate_json(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> dict[str, Any]:
        pass

    async def health_check(self) -> bool:
        return self._is_healthy

    def mark_unhealthy(self) -> None:
        self._is_healthy = False

    def mark_healthy(self) -> None:
        self._is_healthy = True


class OpenAIProvider(BaseProvider):
    def __init__(self, config: ModelConfig | None = None) -> None:
        super().__init__("openai", config or ModelConfig(model_name="gpt-4o-mini"))

    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> str:
        # Provider routing implementation placeholder / API call wrapper
        return f"[OpenAI gpt-4o-mini] Response to: {prompt[:80]}"

    async def generate_json(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> dict[str, Any]:
        return {"provider": "openai", "model": self.config.model_name, "prompt_summary": prompt[:50]}


class AnthropicProvider(BaseProvider):
    def __init__(self, config: ModelConfig | None = None) -> None:
        super().__init__("anthropic", config or ModelConfig(model_name="claude-3-5-sonnet"))

    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> str:
        return f"[Anthropic Claude 3.5 Sonnet] Response to: {prompt[:80]}"

    async def generate_json(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> dict[str, Any]:
        return {"provider": "anthropic", "model": self.config.model_name, "prompt_summary": prompt[:50]}


class GeminiProvider(BaseProvider):
    def __init__(self, config: ModelConfig | None = None) -> None:
        super().__init__("gemini", config or ModelConfig(model_name="gemini-1.5-pro"))

    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> str:
        return f"[Google Gemini 1.5 Pro] Response to: {prompt[:80]}"

    async def generate_json(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> dict[str, Any]:
        return {"provider": "gemini", "model": self.config.model_name, "prompt_summary": prompt[:50]}


class AzureOpenAIProvider(BaseProvider):
    def __init__(self, config: ModelConfig | None = None) -> None:
        super().__init__("azure", config or ModelConfig(model_name="azure-gpt-4o"))

    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> str:
        return f"[Azure OpenAI gpt-4o] Response to: {prompt[:80]}"

    async def generate_json(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> dict[str, Any]:
        return {"provider": "azure", "model": self.config.model_name, "prompt_summary": prompt[:50]}


class OllamaProvider(BaseProvider):
    def __init__(self, config: ModelConfig | None = None) -> None:
        super().__init__("ollama", config or ModelConfig(model_name="llama3.2"))

    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> str:
        return f"[Ollama llama3.2] Response to: {prompt[:80]}"

    async def generate_json(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> dict[str, Any]:
        return {"provider": "ollama", "model": self.config.model_name, "prompt_summary": prompt[:50]}


class MockProvider(BaseProvider):
    def __init__(self, config: ModelConfig | None = None) -> None:
        super().__init__("mock", config or ModelConfig(model_name="mock-v1"))

    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> str:
        return f"[Mock Provider] Response to: {prompt[:80]}"

    async def generate_json(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> dict[str, Any]:
        return {"provider": "mock", "model": self.config.model_name, "prompt_summary": prompt[:50]}
