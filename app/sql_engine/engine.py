
from app.models.semantic import SemanticField


class SQLAIEngine:
    @staticmethod
    def generate_sql(prompt: str, table_name: str, fields: list[SemanticField], dialect: str = "duckdb") -> tuple[str, str, dict[str, str]]:
        prompt_lower = prompt.lower()
        select_cols = []
        mappings = {}

        for field in fields:
            mappings[field.canonical_name] = field.source_column
            if any(term in prompt_lower for term in [field.canonical_name.lower(), field.display_name.lower(), field.source_column.lower()]):
                select_cols.append(f'"{field.source_column}"')

        if not select_cols:
            select_cols = [f'"{f.source_column}"' for f in fields[:5]] if fields else ["*"]

        cols_str = ", ".join(select_cols)
        sql = f'SELECT {cols_str} FROM "{table_name}"'

        if "where" in prompt_lower or "filter" in prompt_lower:
            sql += " WHERE 1=1"
        if "top" in prompt_lower or "limit" in prompt_lower or "first" in prompt_lower:
            sql += " LIMIT 10"

        explanation = f"Query selects semantic fields ({cols_str}) from dataset table {table_name} matching natural language intent."
        return sql, explanation, mappings
