import base64
import hashlib
import json

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import get_settings


def _fernet() -> Fernet:
    secret = get_settings().secret_key.get_secret_value().encode()
    key = base64.urlsafe_b64encode(hashlib.sha256(secret).digest())
    return Fernet(key)


def encrypt_credentials(credentials: dict[str, object]) -> str:
    payload = json.dumps(credentials, separators=(",", ":"), sort_keys=True).encode()
    return _fernet().encrypt(payload).decode()


def decrypt_credentials(value: str | None) -> dict[str, object]:
    if not value:
        return {}
    try:
        return json.loads(_fernet().decrypt(value.encode()))
    except (InvalidToken, json.JSONDecodeError) as exc:
        raise ValueError("Connector credentials cannot be decrypted") from exc
