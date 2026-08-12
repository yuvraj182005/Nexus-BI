from loguru import logger


class AIObservabilityLogger:
    @staticmethod
    def log_invocation(
        agent_name: str,
        prompt_version: str,
        input_tokens: int,
        output_tokens: int,
        duration_ms: float,
        model_name: str = "default-ai-model",
    ) -> None:
        estimated_cost = (input_tokens * 0.0000015) + (output_tokens * 0.000002)
        logger.info(
            f"[AI Observability] Agent={agent_name} Model={model_name} PromptVer={prompt_version} "
            f"TokensIn={input_tokens} TokensOut={output_tokens} Latency={duration_ms:.2f}ms EstCost=${estimated_cost:.6f}"
        )
