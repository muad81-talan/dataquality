def _is_numeric_string(sample_values: list) -> bool:
    if not sample_values:
        return False
    parsed = 0
    for v in sample_values:
        try:
            float(str(v))
            parsed += 1
        except (ValueError, TypeError):
            pass
    return parsed / len(sample_values) > 0.9


def detect(column_metrics: dict, row_count: int) -> list[str]:
    flags = []
    if column_metrics["null_rate"] > 0.5:
        flags.append("high_null_rate")
    if column_metrics["unique_count"] == 1:
        flags.append("constant_column")
    if column_metrics["cardinality_ratio"] > 0.95:
        flags.append("suspected_id")
    if "min" not in column_metrics and _is_numeric_string(column_metrics.get("sample_values", [])):
        flags.append("numeric_as_string")
    return flags
