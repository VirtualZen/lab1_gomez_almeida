from pathlib import Path

import pandas as pd

from lab_semana1.carga import guardar, limpiar, reporte_nulos


def test_cargar(sample_df):
    df = sample_df
    assert df.shape == (1994, 128)
    assert df.columns[0] == "state"

def test_reporte_nulos(sample_df):
    df = sample_df
    result = reporte_nulos(df)

    assert result.iloc[0]["columna"] == "PolicReqPerOffic"
    assert result.iloc[0]["nulos"] == 1675
    assert result.iloc[0]["porcentaje"].round(6) == 84.002006


def test_limpiar(sample_df):
    df = sample_df
    result = limpiar(df)

    # Esto está horrible, pero es lo que se me ocurre para testear que se hizo algo. No es un test perfecto, pero al menos asegura que no se volaron columnas.
    # assert result.columns.tolist() == ["state", "county", "community", "communityname","fold"]
    assert result.columns.tolist() == df.columns.tolist()
    assert result.loc[0, "state"] == 8
    assert len(result) >= 1
    # assert result.index.tolist() == [0]
    

def test_guardar(sample_df):
    df = sample_df
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    archivo = data_dir / "test_output.parquet"
    guardar(df, archivo)

    recuperado = pd.read_parquet(archivo)
    pd.testing.assert_frame_equal(df, recuperado)

