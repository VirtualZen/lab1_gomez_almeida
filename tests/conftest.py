import pytest
from lab_semana1.carga import cargar


@pytest.fixture
def sample_df():
    df = cargar("https://archive.ics.uci.edu/static/public/183/data.csv", na_values=["?"])
    return df