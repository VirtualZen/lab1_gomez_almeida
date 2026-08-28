import numpy as np
import pandas as pd


def filtrar(df: pd.DataFrame, columna: str, umbral: float) -> pd.DataFrame:
    """Mascara booleana: devuelve solo las filas donde df[columna] > umbral."""
    mascara = df[columna] > umbral
    return df[mascara]


def resumen_por_grupo(df: pd.DataFrame, col_grupo: str, cols_num: list) -> pd.DataFrame:
    """Agrupa por col_grupo y calcula media, desviacion estandar y conteo
    para cada columna numerica en cols_num."""
    return df.groupby(col_grupo)[cols_num].agg(["mean", "std", "count"])


def zscore(matriz: np.ndarray) -> np.ndarray:
    """Recibe un np.ndarray 2D y lo normaliza por columna usando broadcasting.
    Prohibido usar un bucle for."""
    return (matriz - matriz.mean(axis=0)) / matriz.std(axis=0)


def top_k(df: pd.DataFrame, columna: str, k: int) -> pd.DataFrame:
    """Los k registros con mayor valor en esa columna, usando np.argsort."""
    indices = np.argsort(df[columna].to_numpy())[::-1][:k]
    return df.iloc[indices]


def recta_minimos_cuadrados(x: np.ndarray, y: np.ndarray) -> tuple:
    """Ajusta y = a*x + b con np.linalg.lstsq y devuelve la tupla (a, b).
    Arma la matriz de diseno apilando x junto a una columna de unos."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    A = np.column_stack([x, np.ones_like(x)])
    (a, b), _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    return a, b