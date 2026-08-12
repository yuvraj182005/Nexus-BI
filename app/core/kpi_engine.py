from typing import Any


class KPIEngine:
    @staticmethod
    def calculate_kpis(data_records: list[dict[str, Any]]) -> dict[str, Any]:
        if not data_records:
            return {"total_records": 0}

        numeric_sums: dict[str, float] = {}
        numeric_counts: dict[str, int] = {}

        for row in data_records:
            for k, v in row.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    numeric_sums[k] = numeric_sums.get(k, 0.0) + float(v)
                    numeric_counts[k] = numeric_counts.get(k, 0) + 1

        kpis: dict[str, Any] = {"total_records": len(data_records)}
        for k in numeric_sums:
            count = numeric_counts[k]
            kpis[f"sum_{k}"] = round(numeric_sums[k], 2)
            kpis[f"avg_{k}"] = round(numeric_sums[k] / count, 2) if count > 0 else 0.0

        return kpis
