import re


class SQLOptimizer:
    @staticmethod
    def analyze(sql: str) -> dict:
        clean = sql.upper()
        joins = []
        indexes = []
        if "JOIN" in clean:
            joins.append("Ensure join key columns have foreign key indexes or hashing indices.")
        if "WHERE" in clean:
            matches = re.findall(r"WHERE\s+([A-Z0-9_]+)", clean)
            for col in matches:
                indexes.append(f"Recommended B-Tree index on column '{col}'.")
        return {
            "estimated_cost": "Low" if len(clean) < 200 else "Medium",
            "join_recommendations": joins,
            "index_recommendations": indexes,
        }
