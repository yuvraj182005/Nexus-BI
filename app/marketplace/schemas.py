from pydantic import BaseModel, Field


class MarketplaceItem(BaseModel):
    item_id: str
    item_type: str  # plugin, connector, dashboard_template, workflow_template, ai_prompt, report_template, visualization_template
    title: str
    description: str
    author: str
    version: str = "1.0.0"
    rating: float = 4.8
    reviews_count: int = 42
    downloads_count: int = 1250
    tags: list[str]
    is_installed: bool = False


class MarketplaceReviewRequest(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0)
    review_text: str
