import uuid
import pytest
from app.identity.mfa import MFAService
from app.identity.providers import EnterpriseSSOProvider
from app.identity.service import global_identity_service


@pytest.mark.asyncio
async def test_sso_providers():
    g_res = await EnterpriseSSOProvider.authenticate_oauth2("google", "mock_code")
    assert g_res["provider"] == "google"
    assert "user@company-domain.com" in g_res["email"]

    e_res = await EnterpriseSSOProvider.authenticate_oauth2("entra_id", "mock_code")
    assert e_res["provider"] == "entra_id"


def test_mfa_setup_and_verify():
    setup = MFAService.setup_mfa("test@nexusbi.ai")
    assert setup.secret is not None
    assert len(setup.backup_codes) == 6

    assert MFAService.verify_mfa("123456", setup.secret) is True
    assert MFAService.verify_mfa("abc", setup.secret) is False


@pytest.mark.asyncio
async def test_service_account_and_pat():
    ws_id = uuid.uuid4()
    sa = await global_identity_service.create_service_account(
        ws_id, type("Req", (), {"name": "CI/CD Pipeline Worker", "role": "analyst", "scopes": ["read"]})()
    )
    assert sa.client_id.startswith("sa_")
    assert sa.client_secret.startswith("sec_")
