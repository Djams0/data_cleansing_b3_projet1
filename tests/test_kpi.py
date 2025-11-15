# tests/test_kpi.py
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils_kpi import kpi_quality, kpi_dicts_to_dataframe

def test_kpi_quality_basic():
    df = pd.DataFrame({
        "a": [1, 2, None],
        "b": ["x", None, "y"]
    })
    res = kpi_quality(df)
    assert res["num_rows"] == 3
    assert res["num_duplicates"] == 0
    assert res["duplicate_rate_pct"] == 0.0
    assert isinstance(res["completeness_per_column"], dict)

def test_kpi_dataframe_conversion():
    before = {"num_rows": 10, "global_completeness_rate": 80, "num_duplicates": 2, "duplicate_rate_pct": 20}
    after  = {"num_rows": 9, "global_completeness_rate": 95, "num_duplicates": 0, "duplicate_rate_pct": 0}

    df = kpi_dicts_to_dataframe(before, after)
    assert list(df["stage"]) == ["Avant", "Apres"]
    assert df.shape[0] == 2
