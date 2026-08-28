import json
from pathlib import Path

import pandas as pd

from lab_semana1.carga import cargar, guardar, limpiar, reporte_nulos
from src.analisis import recta_minimos_cuadrados, resumen_por_grupo, top_k


class FriendlyException(Exception):
    """A concrete exception type with useful metadata and user-friendly display."""

    def __init__(self, message: str = "", *, code: str | None = None, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __str__(self) -> str:
        parts = []
        if self.code:
            parts.append(f"[{self.code}]")
        if self.message:
            parts.append(str(self.message))
        if self.details:
            parts.append(f"details={self.details}")
        return " ".join(parts) if parts else "Exception"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, code={self.code!r}, details={self.details!r})"

    def to_dict(self) -> dict:
        return {
            "message": self.message,
            "code": self.code,
            "details": self.details,
        }


def main():
    url = "https://archive.ics.uci.edu/static/public/183/data.csv"
    print(f"Loading data from {url}")
    df = cargar(url, na_values=["?"])

    print("Generating nulls report...")
    nr = reporte_nulos(df)
    print("Nulls report:")
    print(nr)

    print("Cleaning data (conservative defaults)...")
    cleaned, report = limpiar(df, return_report=True)

    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    cleaned_path = data_dir / "cleaned.parquet"
    print(f"Saving cleaned data to {cleaned_path}")
    guardar(cleaned, cleaned_path)

    report_path = out_dir / "cleaning_report.json"
    print(f"Saving cleaning report to {report_path}")
    with open(report_path, "w", encoding="utf8") as fh:
        json.dump(report, fh, indent=2)

    target = "ViolentCrimesPerPop"

    if "population" in cleaned.columns:
        cleaned["grupo_poblacion"] = pd.qcut(
            cleaned["population"], 4, labels=["Q1", "Q2", "Q3", "Q4"]
        )
        print("Resumen por grupo de poblacion:")
        print(resumen_por_grupo(cleaned, "grupo_poblacion", [target]))
    else:
        print("Columna 'population' no encontrada; se omite resumen_por_grupo.")

    if target in cleaned.columns:
        print(f"Top 5 comunidades por {target}:")
        print(top_k(cleaned, target, 5))
    else:
        print(f"Columna {target} no encontrada; se omite top_k.")

    if "PctPopUnderPov" in cleaned.columns and target in cleaned.columns:
        a, b = recta_minimos_cuadrados(
            cleaned["PctPopUnderPov"].to_numpy(),
            cleaned[target].to_numpy(),
        )
        print(f"Recta de minimos cuadrados: pendiente={a:.4f}, intercepto={b:.4f}")
    else:
        print("Columnas necesarias no encontradas; se omite regresion lineal.")

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping figure.")
    else:
        try:
            if target in cleaned.columns:
                num = cleaned.select_dtypes(include=["number"]).drop(columns=[target], errors="ignore")
                corrs = num.corrwith(cleaned[target]).abs().sort_values(ascending=False).head(10)
                if not corrs.empty:
                    fig_path = out_dir / "figura.png"
                    print(f"Saving figure to {fig_path}")
                    plt.figure(figsize=(8, 4))
                    corrs.plot(kind="bar")
                    plt.title("Top 10 correlaciones absolutas con ViolentCrimesPerPop")
                    plt.tight_layout()
                    plt.savefig(fig_path)
                    plt.close()
            else:
                print(f"Target {target} not in cleaned dataframe; skipping plot.")
        except (RuntimeError, OSError, ValueError) as e:
            print("Plotting failed due to runtime/backend error; skipping figure.", type(e).__name__, e)

    print("Done.")


if __name__ == "__main__":
    main()