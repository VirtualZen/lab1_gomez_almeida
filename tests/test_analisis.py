import numpy as np
import pandas as pd
import pytest

from src.analisis import filtrar, recta_minimos_cuadrados, zscore


@pytest.fixture
def df_mini():
    return pd.DataFrame({
        "grupo": ["a", "a", "b", "b"],
        "valor": [10.0, 20.0, 30.0, 40.0],
    })


def test_filtrar_deja_solo_los_mayores(df_mini):
    resultado = filtrar(df_mini, "valor", 20)
    assert len(resultado) == 2
    assert resultado["valor"].min() > 20


def test_zscore_tiene_media_cero(df_mini):
    z = zscore(df_mini[["valor"]].to_numpy())
    assert z.mean() == pytest.approx(0.0, abs=1e-9)


def test_recta_minimos_cuadrados_puntos_alineados():
    x = np.array([0, 1, 2, 3])
    y = 2 * x + 1
    a, b = recta_minimos_cuadrados(x, y)
    assert a == pytest.approx(2.0)
    assert b == pytest.approx(1.0)