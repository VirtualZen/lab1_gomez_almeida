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

## Pregunta de investigación 2

¿Qué diferencia hay entre correr `pytest` a secas y `uv run pytest`?

`uv run pytest` garantiza que las pruebas se ejecuten con el intérprete y las
dependencias exactas fijadas en `uv.lock` (el `.venv` del proyecto), sin
necesidad de activarlo manualmente. Si en cambio alguien corre `pytest` a
secas sin haber activado ese entorno virtual, puede terminar usando un
Python global del sistema que no tiene instaladas las dependencias del
proyecto (o versiones distintas), y las pruebas fallarían o darían
resultados no reproducibles.