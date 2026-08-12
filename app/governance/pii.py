import re
from typing import Any


class PIIDetector:
    PATTERNS = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "phone": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
        "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    }

    @classmethod
    def scan_dataframe_columns(cls, columns: list[str], sample_values: dict[str, list[Any]]) -> dict[str, list[str]]:
        detected: dict[str, list[str]] = {}

        for col in columns:
            col_lower = col.lower()
            col_findings = set()

            # Header heuristic check
            for pii_type in cls.PATTERNS:
                if pii_type in col_lower:
                    col_findings.add(pii_type)

            # Sample value regex check
            samples = sample_values.get(col, [])
            for val in samples:
                val_str = str(val)
                for pii_type, pattern in cls.PATTERNS.items():
                    if re.search(pattern, val_str):
                        col_findings.add(pii_type)

            if col_findings:
                detected[col] = list(col_findings)

        return detected

    @classmethod
    def mask_value(cls, value: str, pii_type: str) -> str:
        if not value:
            return value
        if pii_type == "email":
            parts = value.split("@")
            if len(parts) == 2:
                return f"{parts[0][0]}***@{parts[1]}"
            return "***@***.com"
        if pii_type in ("ssn", "credit_card", "phone"):
            return f"***-***-{str(value)[-4:]}" if len(str(value)) >= 4 else "*****"
        return "[RESTRICTED PII]"
