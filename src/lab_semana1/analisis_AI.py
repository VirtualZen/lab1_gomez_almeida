"""Funciones de análisis y visualización para el pipeline.

Contiene utilidades pequeñas y reproducibles que Persona B puede usar
para explorar variables, obtener estadísticas y guardar visualizaciones.
"""
from pathlib import Path

import numpy as np
import pandas as pd


def top_correlations(df: pd.DataFrame, target: str, n: int = 10) -> pd.Series:
    """Devuelve las n variables numéricas con mayor correlación absoluta
    respecto a `target`.
    """
    num = df.select_dtypes(include=[np.number])
    if target not in num.columns:
        raise ValueError(f"Target '{target}' no está presente entre las columnas numéricas")
    corrs = num.corrwith(num[target]).abs().drop(labels=[target], errors="ignore")
    return corrs.sort_values(ascending=False).head(n)


def plot_top_correlations(df: pd.DataFrame, target: str, n: int = 10, out_path: str | Path | None = None) -> pd.Series:
    """Calcula y grafica las top-n correlaciones absolutas con `target`."""
    import matplotlib.pyplot as plt

    corrs = top_correlations(df, target, n=n)
    if corrs.empty:
        return corrs

    fig, ax = plt.subplots(figsize=(8, 4))
    corrs.plot(kind="bar", ax=ax)
    ax.set_title(f"Top {len(corrs)} correlaciones absolutas con {target}")
    fig.tight_layout()

    if out_path is not None:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path)
    plt.close(fig)
    return corrs


def summary_statistics(df: pd.DataFrame, numeric_only: bool = True) -> pd.DataFrame:
    """Devuelve estadísticas descriptivas transpuestas para facilitar lectura."""
    if numeric_only:
        return df.describe().T
    return df.describe(include="all").T


def split_features_target(df: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.Series]:
    """Separa X (features) e y (target)."""
    if target not in df.columns:
        raise ValueError(f"Target '{target}' no existe en el DataFrame")
    X = df.drop(columns=[target])
    y = df[target]
    return X, y


__all__ = ["plot_top_correlations", "split_features_target", "summary_statistics", "top_correlations"]
