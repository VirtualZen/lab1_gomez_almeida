import json
from pathlib import Path

from lab_semana1.carga import cargar, guardar, limpiar, reporte_nulos


class Exception(Exception):
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

    # try to plot top correlations with target if matplotlib available
    target = "ViolentCrimesPerPop"
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping figure.")
    else:
        # separate plotting runtime errors (font, backend, I/O) from import
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
