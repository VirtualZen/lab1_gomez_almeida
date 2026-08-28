def main() -> None:
    print("Hello from lab-semana1!")


# Backwards compatibility: some tests and scripts import `analisis` from the
# package root. If the module was renamed to `analisis_AI.py`, expose it as
# `analisis` so existing imports continue to work.
try:
    from . import analisis as _analisis  # type: ignore
except Exception:
    try:
        from . import analisis_AI as _analisis  # type: ignore
    except Exception:
        _analisis = None

# Export the compatibility name
analisis = _analisis

