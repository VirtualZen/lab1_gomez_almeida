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

## Como correr diagnostico datos
uv run pytest -q -s tests/test_check_clean.py::test_counts

## Hallazgos

En la versión inicial
uv run pytest -q -s tests/test_check_clean.py::test_counts no se hace una impieza completa. Se usaron valores configurables

before rows,cols: (1994, 128)
before total NaNs: 39202
before duplicates: 0
after rows,cols: (1994, 107)
after total NaNs: 2351
removed rows: 0
removed cols: 21

Conjunto de datos: 1994 filas y 128 columnas (Communities & Crime, UCI).
Antes del limpiado había 39202 valores NaN; tras aplicar la estrategia conservadora se redujeron a ~2351.
No se encontraron filas duplicadas relevantes en el dataset original.
Aproximadamente 21 columnas fueron eliminadas por tener más del 80% de valores faltantes; entre las columnas con más nulos están PolicReqPerOffic, PolicAveOTWorked, PolicPerPop, RacialMatchCommPol, etc.
La limpieza conservadora conserva la mayoría de las variables útiles y añade indicadores de faltantes para las columnas imputadas.


## Problemas y workarounds
Al correr los comandos de creacion inicial se crearon carpetas lab-semana1 en dos sitios. No se entiende la duplicación.
En el código hay varios .venv y eso causa conflictos y el warning:
`... ... /.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead


## Decisiones de limpieza
Umbrales configurables en la función limpiar():
drop_thresh (por defecto 0.8): eliminar columnas con >80% de valores faltantes.
impute_threshold (por defecto 0.05): solo imputar columnas con ≤5% de faltantes (estrategia conservadora).
Imputación:
Variables numéricas con 0 < missing ≤ impute_threshold: se imputan con la mediana y se añade la columna indicadora <nombre>_was_missing.
Variables categóricas con 0 < missing ≤ impute_threshold: se imputan con la moda y se añade <nombre>_was_missing.
Variables categóricas con missing > impute_threshold: se rellena con el sentinel "missing" y se añade el indicador <nombre>_was_missing.
Registro y reproducibilidad:
limpiar(..., return_report=True) devuelve un report con listas dropped_columns, imputed_numeric, imputed_categorical y recuentos de filas (antes/después). Guardar este report junto a los artefactos del pipeline para trazabilidad.
Razonamiento: la política prioriza conservar columnas estables y evitar introducir sesgo por imputaciones agresivas; los indicadores de faltantes preservan la señal útil para modelos que explotan patrones de missingness.
Cómo ajustar: para conservar más columnas cambiar impute_threshold a valores mayores (ej. 0.2), o para ser más agresivo reducir drop_thresh.

## Pregunta 1
¿por qué uv sync puede reconstruir el entorno aunque .venv/ no esté versionado en el repositorio? ¿Qué archivo se
lo permite y qué guarda exactamente ese archivo? Dos líneas bastan.

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


## Pregunta 2
¿qué diferencia hay entre correr pytest a secas y uv run pytest? Pista: tiene que ver con cuál Python y cuál
entorno terminan ejecutando las pruebas, y con qué pasa si alguien no activó el entorno virtual.

pytest a secas ejecuta el comando pytest que esté en el PATH de la sesión de shell: es decir, usa el intérprete de Python y las dependencias del entorno actualmente activado (por ejemplo, la venv si la activaste). Si no has activado la venv, pytest puede ejecutarse con el Python del sistema y fallar por import errors o por versiones distintas de paquetes.
uv run pytest ejecuta pytest dentro del entorno que gestiona uv según la configuración del proyecto (archivo uv.lock / pyproject.toml). uv crea/usa un entorno reproducible con la versión de Python y las dependencias declaradas, por lo que las pruebas se ejecutan en el mismo intérprete/paquetes en cualquier máquina que use uv, aún si el usuario no activó manualmente la venv.
Consecuencia práctica: si alguien no activó el entorno virtual y ejecuta pytest directamente puede obtener errores tipo ModuleNotFoundError o diferencias por versiones. Con uv run pytest esas discrepancias se evitan porque uv controla cuál Python y qué paquetes se usan.