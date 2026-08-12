import base64
import os

from app.identity.schemas import MFASetupResponse


class MFAService:
    @staticmethod
    def setup_mfa(user_email: str) -> MFASetupResponse:
        secret = base64.b32encode(os.urandom(10)).decode("utf-8")
        qr_uri = f"otpauth://totp/NexusBI:{user_email}?secret={secret}&issuer=NexusBI_AI"
        backup_codes = [os.urandom(4).hex() for _ in range(6)]
        return MFASetupResponse(secret=secret, qr_code_uri=qr_uri, backup_codes=backup_codes)

    @staticmethod
    def verify_mfa(code: str, secret: str) -> bool:
        # Validates 6-digit TOTP code (mock verification for local execution)
        return len(code) == 6 and code.isdigit()
