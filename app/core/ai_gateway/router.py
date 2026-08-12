import time

from app.core.ai_gateway.config import GatewayConfig
from app.core.ai_gateway.providers import (
    AnthropicProvider,
    AzureOpenAIProvider,
    BaseProvider,
    GeminiProvider,
    MockProvider,
    OllamaProvider,
    OpenAIProvider,
)


class RateLimiter:
    def __init__(self, requests_per_minute: int = 600) -> None:
        self.rpm = requests_per_minute
        self._timestamps: list[float] = []

    def check_and_record(self) -> bool:
        now = time.time()
        self._timestamps = [t for t in self._timestamps if now - t < 60.0]
        if len(self._timestamps) >= self.rpm:
            return False
        self._timestamps.append(now)
        return True


class ProviderRouter:
    def __init__(self, config: GatewayConfig | None = None) -> None:
        self.config = config or GatewayConfig()
        self.rate_limiter = RateLimiter(self.config.rate_limit_per_minute)
        self.providers: dict[str, BaseProvider] = {
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "gemini": GeminiProvider(),
            "azure": AzureOpenAIProvider(),
            "ollama": OllamaProvider(),
            "mock": MockProvider(),
        }

    def get_provider(self, name: str) -> BaseProvider | None:
        return self.providers.get(name.lower())

    async def select_healthy_provider(self, preferred_provider: str | None = None) -> BaseProvider:
        if not self.rate_limiter.check_and_record():
            raise RuntimeError("AI Gateway Rate Limit Exceeded")

        candidates = list(self.config.fallback_chain)
        if preferred_provider and preferred_provider.lower() in self.providers:
            candidates.insert(0, preferred_provider.lower())

        for name in candidates:
            provider = self.providers.get(name)
            if provider and await provider.health_check():
                return provider

        # Fallback to mock provider guaranteed
        return self.providers["mock"]

    async def check_all_health(self) -> dict[str, bool]:
        health_status = {}
        for name, provider in self.providers.items():
            health_status[name] = await provider.health_check()
        return health_status
