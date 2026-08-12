import re

FORBIDDEN_KEYWORDS = [
    "DROP",
    "DELETE",
    "UPDATE",
    "ALTER",
    "TRUNCATE",
    "INSERT",
    "GRANT",
    "REVOKE",
    "EXEC",
    "EXECUTE",
]


class SQLValidator:
    @staticmethod
    def validate_read_only(sql: str, allow_mutation: bool = False) -> tuple[bool, str | None]:
        clean_sql = re.sub(r"--.*?\n", "", sql)
        clean_sql = re.sub(r"/\*.*?\*/", "", clean_sql, flags=re.DOTALL).upper()
        tokens = re.findall(r"\b[A-Z]+\b", clean_sql)

        if not allow_mutation:
            for kw in FORBIDDEN_KEYWORDS:
                if kw in tokens:
                    return False, f"Dangerous operation '{kw}' detected. SQL engine is in read-only mode."

        if not clean_sql.strip().startswith("SELECT") and not clean_sql.strip().startswith("WITH"):
            return False, "Query must begin with SELECT or WITH."

        return True, None
