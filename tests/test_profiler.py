import pandas as pd
from app.profiler import profile


def make_df():
    return pd.DataFrame({
        "id": [1, 2, 3, 2],
        "name": ["alice", "bob", "charlie", "bob"],
        "score": [10.0, 20.0, 30.0, 20.0],
    })


def test_dataset_row_count():
    result = profile(make_df(), file_size_bytes=100)
    assert result["dataset"]["row_count"] == 4


def test_dataset_col_count():
    result = profile(make_df(), file_size_bytes=100)
    assert result["dataset"]["col_count"] == 3


def test_dataset_duplicate_rows():
    result = profile(make_df(), file_size_bytes=100)
    assert result["dataset"]["duplicate_rows"] == 1


def test_dataset_file_size():
    result = profile(make_df(), file_size_bytes=2048)
    assert result["dataset"]["file_size_bytes"] == 2048


def test_column_null_rate():
    df = pd.DataFrame({"x": [1, None, None, None]})
    result = profile(df, file_size_bytes=100)
    col = result["columns"]["x"]
    assert col["null_count"] == 3
    assert col["null_rate"] == 0.75


def test_column_cardinality():
    df = pd.DataFrame({"cat": ["a", "b", "a", "c"]})
    result = profile(df, file_size_bytes=100)
    col = result["columns"]["cat"]
    assert col["unique_count"] == 3
    assert col["cardinality_ratio"] == 0.75


def test_numeric_stats():
    df = pd.DataFrame({"score": [10.0, 20.0, 30.0, 40.0]})
    result = profile(df, file_size_bytes=100)
    col = result["columns"]["score"]
    assert col["min"] == 10.0
    assert col["max"] == 40.0
    assert col["mean"] == 25.0
    assert col["std"] is not None


def test_no_numeric_stats_for_string_column():
    df = pd.DataFrame({"name": ["alice", "bob"]})
    result = profile(df, file_size_bytes=100)
    col = result["columns"]["name"]
    assert "min" not in col
    assert "max" not in col
    assert "mean" not in col
    assert "std" not in col


def test_top_values():
    df = pd.DataFrame({"cat": ["a", "a", "b", "c", "a", "b"]})
    result = profile(df, file_size_bytes=100)
    top = result["columns"]["cat"]["top_values"]
    assert top[0] == {"value": "a", "count": 3}
    assert top[1] == {"value": "b", "count": 2}
    assert len(top) <= 10


def test_sample_values():
    df = pd.DataFrame({"x": [10, 20, 30, 40, 50, 60]})
    result = profile(df, file_size_bytes=100)
    samples = result["columns"]["x"]["sample_values"]
    assert len(samples) <= 5
    assert all(s in [10, 20, 30, 40, 50, 60] for s in samples)


def test_column_dtype():
    df = pd.DataFrame({"num": [1, 2, 3], "text": ["a", "b", "c"]})
    result = profile(df, file_size_bytes=100)
    assert result["columns"]["num"]["dtype"] == "numeric"
    assert result["columns"]["text"]["dtype"] == "string"
