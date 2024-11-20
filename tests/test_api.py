import pytest
import requests

import os
from dotenv import load_dotenv
import os

load_dotenv()

mongodb_url = os.getenv("MONGODB_URL")
api_url = os.getenv("API_URL")
meteo_api_url = eval(os.getenv("API_URL_METEO_2"))
meteo_api_key = os.getenv("METEO_API_KEY")

headers = {
        "Authorization": f"Bearer {meteo_api_key}",  # ou "x-api-key": api_key, selon l'API
        "Content-Type": "application/json",  # souvent nécessaire si vous envoyez des données JSON
    }


@pytest.fixture
def headers():
    return {
        "Authorization": f"Bearer {meteo_api_key}",  # ou "x-api-key": api_key, selon l'API
        "Content-Type": "application/json",  # souvent nécessaire si vous envoyez des données JSON
    }

def test_api_meteo(headers):
    response = requests.get(f"{meteo_api_url}", headers=headers)
    assert response.status_code == 200
    assert len(response.content) > 0


def test_api_conso():
    response = requests.get(f"{api_url}")
    assert response.status_code == 200
    assert len(response.content) > 0
