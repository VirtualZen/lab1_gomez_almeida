# Lab Semana 1 - Communities and Crime

- Persona A: Paul Gomez Ehmig
- Persona B: Ronnie Almeida
- Dataset: https://archive.ics.uci.edu/static/public/183/data.csv
- Tarea: regresión
  Variable objetivo predicción: ViolentCrimesPerPop
- Descripción: Comunidades de EE.UU. los datos combinan información socioeconómica del censo de 1990, datos policiales de la encuesta LEMAS de 1990 y datos de crimen de la UCR del FBI de 1995. (fuente: https://archive.ics.uci.edu/dataset/183/communities+and+crime)
- Motivo: Elegimos este dataset porque combina variables socioeconómicas y demográficas con tasas de criminalidad, y tiene ~39000 faltantes repartidos en 25 columnas de diferentes tipos, lo que da material real para practicar la limpieza.

## Como correr
uv sync
uv run pytest -q
uv run python main.py

tmpdir=$(mktemp -d /tmp/uv-cache-XXXXX) && export UV_CACHE_DIR="$tmpdir" && PYTHONPATH=src uv run --active pytest -v
tmpdir=$(mktemp -d /tmp/uv-cache-XXXXX) && export UV_CACHE_DIR="$tmpdir" && PYTHONPATH=src uv run pytest -v



## Hallazgos

## Decisiones de limpieza