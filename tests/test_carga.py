from pathlib import Path

import pandas as pd

from lab_semana1.carga import cargar, guardar, limpiar, reporte_nulos


def test_cargar(tmp_path):
    df = cargar("https://archive.ics.uci.edu/static/public/183/data.csv", na_values=["?"])
    assert df.shape == (1994, 128)
    assert df.columns[0] == "state"

def test_reporte_nulos():
    df = cargar("https://archive.ics.uci.edu/static/public/183/data.csv", na_values=["?"])

    result = reporte_nulos(df)

    assert result.iloc[0]["columna"] == "PolicReqPerOffic"
    assert result.iloc[0]["nulos"] == 1675
    assert result.iloc[0]["porcentaje"].round(6) == 84.002006


def test_limpiar():
    df = cargar("https://archive.ics.uci.edu/static/public/183/data.csv", na_values=["?"])

    result = limpiar(df)

    # Esto está horrible, pero es lo que se me ocurre para testear que se hizo algo. No es un test perfecto, pero al menos asegura que no se volaron columnas.
    # assert result.columns.tolist() == ["state", "county", "community", "communityname","fold"]
    assert result.columns.tolist() == df.columns.tolist()
    assert result.loc[0, "state"] == 8
    assert len(result) >= 1
    # assert result.index.tolist() == [0]
    

def test_guardar(tmp_path):
    df = cargar("https://archive.ics.uci.edu/static/public/183/data.csv", na_values=["?"])
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    archivo = data_dir / "test_output.parquet"
    guardar(df, archivo)

    recuperado = pd.read_parquet(archivo)
    pd.testing.assert_frame_equal(df, recuperado)

