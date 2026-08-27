def test_counts():
    from lab_semana1.carga import cargar, limpiar
    url = "https://archive.ics.uci.edu/static/public/183/data.csv"
    df = cargar(url, na_values=["?"])
    print(f"before rows,cols: {df.shape}")
    print(f"before total NaNs: {int(df.isna().sum().sum())}")
    print(f"before duplicates: {int(df.duplicated().sum())}")
    clean = limpiar(df)
    print(f"after rows,cols: {clean.shape}")
    print(f"after total NaNs: {int(clean.isna().sum().sum())}")
    assert True
