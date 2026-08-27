
import numpy as np
import pandas as pd


def dummy():
    """Dummy function placeholder for syntax."""
    return []


def cargar(url, na_values=None):
    """pd.read_csv desde la URL. El parámetro na_values es lo que les permite
    decirle a pandas que '?' o -200 son faltantes desde la lectura.
    
    Args:
        url (str): The URL or file path to the CSV file.
        na_values (list, optional): Additional strings to recognize as NA/NaN. Defaults to None.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """

    result = pd.read_csv(url, na_values=na_values)
    return result



def reporte_nulos(df):
    """Devuelve un DataFrame con una fila por columa:
    conteo de nulos y porcentaje, ordenado de mayor a menor.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.DataFrame: A DataFrame containing the count of null values for each column.
    """

    null_count = df.isna().sum()
    null_percentage = (null_count.values / len(df)) * 100
    result = pd.DataFrame({
        "columna": null_count.index,
        "nulos": null_count.values,
        "porcentaje": null_percentage
    }).sort_values("nulos", ascending=False).reset_index(drop=True)
    return result


def limpiar(df):
    """En este orden:
    replace([np.inf, -np.inf], np.nan),
    drop_duplicates(),
    .str.strip().str.lower()
    en las columnas de texto,
    y tratar los faltantes columna por columna.
    Cierra con reset_index(drop=True).
    
    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    
    result = df.copy()
    result = result.replace([np.inf, -np.inf], np.nan)
    result = result.drop_duplicates()

    # text_columns = result.select_dtypes(include="object").columns
    text_columns = result.select_dtypes(include=["object", "string"]).columns
    result[text_columns] = result[text_columns].apply(
        lambda column: column.str.strip().str.lower()
        )
    # Apply the missing-value rule required by the assignment here.
    # result.fillna(method='ffill', inplace=True)
    return result.reset_index(drop=True)


def guardar(df, ruta):
    """Guardar el resultado en formato Parquet con to_parquet.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        ruta (str): The file path where the CSV will be saved.
    """
    df.to_parquet(ruta, index=False)
