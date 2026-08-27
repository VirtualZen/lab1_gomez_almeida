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

## Hallazgos

## Decisiones de limpieza

## Pregunta 1
uv.lock contiene información de runtime, dependencias y paquetes requeridos
uv sync puede reconstruir el entorno porque uv.lock sí está versionado en el repositorio
y guarda las versiones exactas (con hash) de cada dependencia resuelta a partir de pyproject.toml,
así que uv solo necesita descargarlas e instalarlas para recrear .venv/ de forma idéntica.
muestra:
version = 1
revision = 3
requires-python = ">=3.14"
 ...
[[package]]
name = "numpy"
version = "2.5.2"