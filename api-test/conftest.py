import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    """Retorna a URL base para a API."""
    return "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def api_client():
    """Retorna um cliente de API (requests.Session) para toda a sessão."""
    return requests.Session()
