import asyncio
import time
from typing import Any

from app.core.ai_gateway.config import GatewayConfig
from app.core.ai_gateway.router import ProviderRouter
from app.core.observability import AIObservabilityLogger


class AIGatewayResponse:
    def __init__(self, text: str) -> None:
        self.text = text

    def __str__(self) -> str:
        return self.text


class AIGateway:
    def __init__(self, config: GatewayConfig | None = None) -> None:
        self.config = config or GatewayConfig()
        self.router = ProviderRouter(self.config)

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        preferred_provider: str | None = None,
        service_context: str = "GeneralService",
        **kwargs: Any,
    ) -> AIGatewayResponse:
        text = await self.generate_text(prompt, system_prompt, preferred_provider, service_context, **kwargs)
        return AIGatewayResponse(text)

    async def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        preferred_provider: str | None = None,
        service_context: str = "GeneralService",
        **kwargs: Any,
    ) -> str:
        provider = await self.router.select_healthy_provider(preferred_provider)
        start_time = time.time()
        retries = 0
        last_error = None

        while retries <= self.config.max_retries:
            try:
                res = await asyncio.wait_for(
                    provider.generate_text(prompt, system_prompt, **kwargs),
                    timeout=provider.config.timeout_seconds,
                )
                duration_ms = (time.time() - start_time) * 1000.0

                # Token & cost estimation tracking
                input_tokens = len(prompt.split()) + (len(system_prompt.split()) if system_prompt else 0)
                output_tokens = len(res.split())
                cost = (input_tokens * provider.config.input_cost_per_token) + (
                    output_tokens * provider.config.output_cost_per_token
                )

                AIObservabilityLogger.log_invocation(
                    agent_name=service_context,
                    prompt_version="gateway-v1",
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    duration_ms=duration_ms,
                    model_name=f"{provider.name}:{provider.config.model_name}",
                )
                return res
            except Exception as exc:
                last_error = exc
                retries += 1
                if retries <= self.config.max_retries:
                    await asyncio.sleep(0.1 * (2 ** (retries - 1)))
                else:
                    provider.mark_unhealthy()
                    # Fallback to mock on retry failure
                    mock_provider = self.router.providers["mock"]
                    res = await mock_provider.generate_text(prompt, system_prompt, **kwargs)
                    return res

        return f"[Fallback Response] Prompt processed with warning: {last_error}"

    async def generate_json(
        self,
        prompt: str,
        system_prompt: str | None = None,
        preferred_provider: str | None = None,
        service_context: str = "GeneralService",
        **kwargs: Any,
    ) -> dict[str, Any]:
        provider = await self.router.select_healthy_provider(preferred_provider)
        start_time = time.time()

        try:
            res = await asyncio.wait_for(
                provider.generate_json(prompt, system_prompt, **kwargs),
                timeout=provider.config.timeout_seconds,
            )
            duration_ms = (time.time() - start_time) * 1000.0

            AIObservabilityLogger.log_invocation(
                agent_name=service_context,
                prompt_version="gateway-v1",
                input_tokens=len(prompt.split()),
                output_tokens=50,
                duration_ms=duration_ms,
                model_name=f"{provider.name}:{provider.config.model_name}",
            )
            return res
        except Exception:
            mock_provider = self.router.providers["mock"]
            return await mock_provider.generate_json(prompt, system_prompt, **kwargs)


# Global singleton instance
global_ai_gateway = AIGateway()
