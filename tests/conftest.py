import pytest
import requests


@pytest.fixture
def api_session():
    """Provide a reusable HTTP session for API tests."""
    session = requests.Session()
    yield session
    session.close()