import matplotlib
import pandas as pd

matplotlib.use("Agg")

from lab_semana1 import analisis


def test_top_correlations():
    df = pd.DataFrame({
        "target": [1, 2, 3, 4, 5],
        "a": [2, 4, 6, 8, 10],
        "b": [5, 4, 3, 2, 1],
        "c": [1, 1, 2, 2, 1],
    })
    res = analisis.top_correlations(df, "target", n=2)
    assert set(res.index) == {"a", "b"}
    assert len(res) == 2


def test_plot_top_correlations(tmp_path):
    df = pd.DataFrame({
        "target": [1, 2, 3, 4, 5],
        "a": [2, 4, 6, 8, 10],
        "b": [5, 4, 3, 2, 1],
    })
    out = tmp_path / "fig.png"
    res = analisis.plot_top_correlations(df, "target", n=2, out_path=out)
    assert out.exists()
    assert not res.empty


def test_summary_statistics():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6], "cat": ["a", "b", "a"]})
    num = analisis.summary_statistics(df, numeric_only=True)
    assert "x" in num.index
    allstats = analisis.summary_statistics(df, numeric_only=False)
    assert "cat" in allstats.index


def test_split_features_target():
    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    X, y = analisis.split_features_target(df, "y")
    assert "y" not in X.columns
    assert y.equals(df["y"]) 
    import pytest

    with pytest.raises(ValueError):
        analisis.split_features_target(df, "z")
