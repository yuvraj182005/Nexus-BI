import uuid
import pytest
from app.saas.service import global_saas_service


def test_saas_workspace_usage():
    ws_id = uuid.uuid4()
    usage = global_saas_service.get_workspace_usage(ws_id)
    assert usage.current_plan == "Pro"
    assert usage.storage_limit_mb == 10000.0
    assert usage.billing_status == "active"


def test_payment_webhook_invoicing():
    ws_id = uuid.uuid4()
    inv = global_saas_service.process_payment_webhook(ws_id, "payment_intent.succeeded", 49.0)
    assert inv.status == "paid"
    assert inv.amount_usd == 49.0
