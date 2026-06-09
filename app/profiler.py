import pandas as pd


def _profile_column(series: pd.Series, row_count: int) -> dict:
    null_count = int(series.isna().sum())
    unique_count = int(series.nunique())
    if pd.api.types.is_numeric_dtype(series):
        dtype = "numeric"
    elif pd.api.types.is_datetime64_any_dtype(series):
        dtype = "datetime"
    elif pd.api.types.is_bool_dtype(series):
        dtype = "boolean"
    else:
        dtype = "string"
    col: dict = {
        "dtype": dtype,
        "null_count": null_count,
        "null_rate": null_count / row_count if row_count else 0.0,
        "unique_count": unique_count,
        "cardinality_ratio": unique_count / row_count if row_count else 0.0,
    }
    if dtype == "numeric":
        col["min"] = float(series.min())
        col["max"] = float(series.max())
        col["mean"] = float(series.mean())
        col["std"] = float(series.std())
    top = series.value_counts().head(10)
    col["top_values"] = [{"value": v, "count": int(c)} for v, c in top.items()]
    col["sample_values"] = series.dropna().head(5).tolist()
    return col


def profile(df: pd.DataFrame, file_size_bytes: int) -> dict:
    return {
        "dataset": {
            "row_count": len(df),
            "col_count": len(df.columns),
            "duplicate_rows": int(df.duplicated().sum()),
            "file_size_bytes": file_size_bytes,
        },
        "columns": {col: _profile_column(df[col], len(df)) for col in df.columns},
    }
