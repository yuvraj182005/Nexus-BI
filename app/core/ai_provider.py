import abc
from typing import Any

from app.core.ai_gateway import global_ai_gateway


class BaseAIProvider(abc.ABC):
    @abc.abstractmethod
    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> str:
        pass

    @abc.abstractmethod
    async def generate_json(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> dict[str, Any]:
        pass


class GatewayAIProviderAdapter(BaseAIProvider):
    def __init__(self, provider_type: str = "mock") -> None:
        self.provider_type = provider_type

    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> str:
        return await global_ai_gateway.generate_text(
            prompt, system_prompt=system_prompt, preferred_provider=self.provider_type, **kwargs
        )

    async def generate_json(self, prompt: str, system_prompt: str | None = None, **kwargs: Any) -> dict[str, Any]:
        return await global_ai_gateway.generate_json(
            prompt, system_prompt=system_prompt, preferred_provider=self.provider_type, **kwargs
        )


def get_ai_provider(provider_type: str = "mock") -> BaseAIProvider:
    return GatewayAIProviderAdapter(provider_type)
