import pytest
from app.governance.pii import PIIDetector


def test_pii_detection_regex():
    cols = ["email_address", "phone_number", "ssn_code", "revenue"]
    samples = {
        "email_address": ["alice@example.com"],
        "phone_number": ["555-0199"],
        "ssn_code": ["123-45-6789"],
        "revenue": [100.0],
    }

    detected = PIIDetector.scan_dataframe_columns(cols, samples)
    assert "email_address" in detected
    assert "email" in detected["email_address"]
    assert "phone_number" in detected
    assert "ssn_code" in detected
    assert "revenue" not in detected


def test_pii_masking():
    masked_email = PIIDetector.mask_value("john.doe@example.com", "email")
    assert masked_email == "j***@example.com"

    masked_ssn = PIIDetector.mask_value("123-45-6789", "ssn")
    assert masked_ssn == "***-***-6789"
