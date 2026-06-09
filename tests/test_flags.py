import pandas as pd
from app.profiler import profile
from app.flags import detect


def col_metrics(series):
    df = pd.DataFrame({"x": series})
    return profile(df, file_size_bytes=100)["columns"]["x"]


def test_high_null_rate_flagged():
    metrics = col_metrics([None, None, None, 1])
    assert "high_null_rate" in detect(metrics, row_count=4)


def test_high_null_rate_not_flagged_below_threshold():
    metrics = col_metrics([1, 2, None, 4])
    assert "high_null_rate" not in detect(metrics, row_count=4)


def test_constant_column_flagged():
    metrics = col_metrics(["x", "x", "x", "x"])
    assert "constant_column" in detect(metrics, row_count=4)


def test_constant_column_not_flagged():
    metrics = col_metrics(["x", "y", "x", "z"])
    assert "constant_column" not in detect(metrics, row_count=4)


def test_suspected_id_flagged():
    metrics = col_metrics([1, 2, 3, 4])
    assert "suspected_id" in detect(metrics, row_count=4)


def test_suspected_id_not_flagged():
    metrics = col_metrics(["a", "b", "a", "b"])
    assert "suspected_id" not in detect(metrics, row_count=4)


def test_numeric_as_string_flagged():
    metrics = col_metrics(["1", "2", "3", "4"])
    assert "numeric_as_string" in detect(metrics, row_count=4)


def test_numeric_as_string_not_flagged_for_real_strings():
    metrics = col_metrics(["alice", "bob", "charlie", "dave"])
    assert "numeric_as_string" not in detect(metrics, row_count=4)
