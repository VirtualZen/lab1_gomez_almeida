from lab_semana1.carga import cargar, limpiar

url = "https://archive.ics.uci.edu/static/public/183/data.csv"
print(f"Loading dataset from: {url}")
df = cargar(url, na_values=["?"])

before_shape = df.shape
before_nans = int(df.isna().sum().sum())
before_dups = int(df.duplicated().sum())

print(f"Before: rows={before_shape[0]}, cols={before_shape[1]}")
print(f"Before total NaNs: {before_nans}")
print(f"Before duplicate rows: {before_dups}")

clean = limpiar(df)
after_shape = clean.shape
after_nans = int(clean.isna().sum().sum())

print(f"After: rows={after_shape[0]}, cols={after_shape[1]}")
print(f"After total NaNs: {after_nans}")
print(f"Rows removed: {before_shape[0] - after_shape[0]}")

# Show top 5 columns with most nans before and after
nulls_before = df.isna().sum().sort_values(ascending=False).head(10)
nulls_after = clean.isna().sum().sort_values(ascending=False).head(10)
print('\nTop nulls before:\n', nulls_before)
print('\nTop nulls after:\n', nulls_after)
