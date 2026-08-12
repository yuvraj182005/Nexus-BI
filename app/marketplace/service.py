from app.marketplace.schemas import MarketplaceItem, MarketplaceReviewRequest


class MarketplaceService:
    def __init__(self) -> None:
        self._seed_marketplace()

    def _seed_marketplace(self) -> None:
        self.catalog: list[MarketplaceItem] = [
            MarketplaceItem(
                item_id="mp_snowflake_connector",
                item_type="connector",
                title="Snowflake Enterprise Connector",
                description="High-throughput Snowflake warehouse reader with auto-OAuth2 refresh",
                author="NexusBI Core Team",
                version="2.1.0",
                rating=4.9,
                reviews_count=128,
                downloads_count=4500,
                tags=["snowflake", "warehouse", "database"],
            ),
            MarketplaceItem(
                item_id="mp_exec_dashboard_tpl",
                item_type="dashboard_template",
                title="C-Suite Executive Financial Overview",
                description="Pre-configured Plotly dashboard grid with gross margin and revenue KPIs",
                author="FinTech Analytics Inc.",
                version="1.4.0",
                rating=4.8,
                reviews_count=85,
                downloads_count=3200,
                tags=["financial", "c-suite", "dashboard"],
            ),
            MarketplaceItem(
                item_id="mp_deepar_forecast_plugin",
                item_type="plugin",
                title="DeepAR Time-Series ML Forecaster",
                description="Deep learning probabilistic forecast model plugin",
                author="ML Partner Labs",
                version="1.0.2",
                rating=4.7,
                reviews_count=34,
                downloads_count=1100,
                tags=["ml", "deepar", "forecast"],
            ),
            MarketplaceItem(
                item_id="mp_prompt_cfo_advisor",
                item_type="ai_prompt",
                title="CFO Strategic Advisory System Prompt",
                description="Optimized LLM prompt for financial decision synthesis",
                author="PromptCraft Studio",
                version="3.0.0",
                rating=5.0,
                reviews_count=67,
                downloads_count=2800,
                tags=["prompt", "cfo", "finance"],
            ),
        ]

    def list_items(self, item_type: str | None = None) -> list[MarketplaceItem]:
        if item_type:
            return [i for i in self.catalog if i.item_type == item_type]
        return list(self.catalog)

    def install_item(self, item_id: str) -> MarketplaceItem:
        for item in self.catalog:
            if item.item_id == item_id:
                item.is_installed = True
                item.downloads_count += 1
                return item
        raise ValueError(f"Marketplace item '{item_id}' not found")

    def submit_review(self, item_id: str, request: MarketplaceReviewRequest) -> MarketplaceItem:
        for item in self.catalog:
            if item.item_id == item_id:
                item.reviews_count += 1
                # Recalculate average rating
                item.rating = round(((item.rating * (item.reviews_count - 1)) + request.rating) / item.reviews_count, 2)
                return item
        raise ValueError(f"Marketplace item '{item_id}' not found")


global_marketplace_service = MarketplaceService()
