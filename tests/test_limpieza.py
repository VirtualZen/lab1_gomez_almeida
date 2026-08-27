from lab_semana1.carga import cargar, limpiar


def test_limpieza_report():
    url = "https://archive.ics.uci.edu/static/public/183/data.csv"
    df = cargar(url, na_values=["?"])

    # run cleaning with a report
    cleaned, report = limpiar(df, drop_threshold=0.8, impute_threshold=0.05, return_report=True)

    # expected dropped columns: those with > drop_thresh fraction missing in original
    expected_dropped = sorted([c for c in df.columns if df[c].isna().mean() > 0.8])
    assert sorted(report["dropped_columns"]) == expected_dropped

    # expected imputed numeric: numeric cols with 0 < miss_frac <= impute_thresh
    expected_imputed_num = sorted([
        c for c in df.select_dtypes(include="number").columns
        if 0 < df[c].isna().mean() <= 0.05 and c in cleaned.columns
    ])
    assert sorted(report["imputed_numeric"]) == expected_imputed_num

    # basic sanity: dropped columns are not present in cleaned
    for c in report["dropped_columns"]:
        assert c not in cleaned.columns

    # check indicators: for each imputed column there should be a <col>_was_missing
    for c in report["imputed_numeric"] + report["imputed_categorical"]:
        assert f"{c}_was_missing" in cleaned.columns
