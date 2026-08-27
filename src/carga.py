def dummy():
    """Dummy function placeholder for syntax."""
    return []


def cargar(url, na_values=None):
    """pd.read_csv desde la URL. El parámetro na_values es lo que les permite decirle a pandas que '?' o -200 son faltantes desde la lectura.

    Args:
        url (str): The URL or file path to the CSV file.
        na_values (list, optional): Additional strings to recognize as NA/NaN. Defaults to None.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    return None


def reporte_nulos(df):
    """Devuelve un DataFrame con una fila por columa: conteo de nulos y porcentaje, ordenado de mayor a menor.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.DataFrame: A DataFrame containing the count of null values for each column.
    """
    return None


def limpiar(df):
    """En este orden: replace([np.inf, -np.inf], np.nan), drop_duplicates(), .str.strip().str.lower() en las columnas de texto, y tratar los faltantes columna por columna. Cierra con reset_index(drop=True).

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    return df

def guardar(df, ruta):
    """Guardar el resultado en formato Parquet con to_parquet.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        ruta (str): The file path where the CSV will be saved.
    """
    return None