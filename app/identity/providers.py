from typing import Any


class EnterpriseSSOProvider:
    @staticmethod
    async def authenticate_oauth2(provider: str, code_or_token: str) -> dict[str, Any]:
        p = provider.lower()
        if p in ("google", "google_workspace"):
            return {
                "provider": "google",
                "email": "user@company-domain.com",
                "name": "Google Workspace User",
                "external_id": "google_123456",
            }
        elif p == "github":
            return {
                "provider": "github",
                "email": "developer@github.com",
                "name": "GitHub Developer",
                "external_id": "gh_78910",
            }
        elif p in ("entra_id", "azure_ad"):
            return {
                "provider": "entra_id",
                "email": "employee@enterprise-tenant.onmicrosoft.com",
                "name": "Entra ID Enterprise User",
                "external_id": "azure_aad_998877",
            }
        elif p == "ldap":
            return {
                "provider": "ldap",
                "email": "sysadmin@corp.internal",
                "name": "LDAP Internal User",
                "external_id": "ldap_uid_1001",
            }
        else:
            return {
                "provider": "oidc_generic",
                "email": "user@oidc-provider.org",
                "name": "OpenID Connect User",
                "external_id": "oidc_sub_554433",
            }
