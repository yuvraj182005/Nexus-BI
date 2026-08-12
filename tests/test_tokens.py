from datetime import timedelta

from app.auth.security import TokenType, create_token, decode_token


def test_access_token_round_trip() -> None:
    token = create_token("user-123", TokenType.ACCESS, timedelta(minutes=5))
    payload = decode_token(token, TokenType.ACCESS)

    assert payload["sub"] == "user-123"
    assert payload["type"] == TokenType.ACCESS.value
