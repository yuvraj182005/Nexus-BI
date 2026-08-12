import re


class SecurityHardeningService:
    PROMPT_INJECTION_PATTERNS = [
        r"ignore\s+all\s+previous\s+instructions",
        r"system\s+prompt\s+override",
        r"you\s+are\s+now\s+DAN",
        r"reveal\s+secret\s+key",
        r"bypass\s+security",
    ]

    @classmethod
    def sanitize_input_prompt(cls, prompt: str) -> tuple[str, bool]:
        """Scans for Prompt Injection and RAG Poisoning attacks."""
        for pattern in cls.PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                return "[BLOCKED PROMPT INJECTION DETECTED]", True
        return prompt, False

    @classmethod
    def sanitize_xss(cls, html_or_text: str) -> str:
        """Removes script tags and unsafe HTML attributes."""
        clean = re.sub(r"<script.*?>.*?</script>", "", html_or_text, flags=re.DOTALL | re.IGNORECASE)
        clean = re.sub(r"javascript:", "", clean, flags=re.IGNORECASE)
        clean = re.sub(r"onload=", "", clean, flags=re.IGNORECASE)
        return clean

    @classmethod
    def validate_file_upload(cls, filename: str, content: bytes) -> tuple[bool, str | None]:
        """Validates file extensions and scans for malware/executable signatures."""
        allowed_exts = {".csv", ".parquet", ".json", ".xlsx", ".txt"}
        lower_name = filename.lower()
        if not any(lower_name.endswith(ext) for ext in allowed_exts):
            return False, f"File extension not permitted. Allowed: {allowed_exts}"

        # Malware / Executable header signature check
        if content.startswith(b"MZ") or content.startswith(b"\x7fELF") or b"<script>" in content.lower():
            return False, "Malware or executable code signature detected in uploaded file."

        return True, None


global_security_service = SecurityHardeningService()
