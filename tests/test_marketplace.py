import pytest
from app.marketplace.schemas import MarketplaceReviewRequest
from app.marketplace.service import global_marketplace_service


def test_marketplace_listing_and_installation():
    items = global_marketplace_service.list_items("connector")
    assert len(items) >= 1
    assert items[0].item_id == "mp_snowflake_connector"

    installed = global_marketplace_service.install_item("mp_snowflake_connector")
    assert installed.is_installed is True


def test_marketplace_reviews():
    item = global_marketplace_service.submit_review("mp_exec_dashboard_tpl", MarketplaceReviewRequest(rating=5.0, review_text="Excellent dashboard template!"))
    assert item.reviews_count >= 86
