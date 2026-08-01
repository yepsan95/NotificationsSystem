import pytest
from fastapi import status
from fastapi.testclient import TestClient
from src.database.real_database import get_db
from tests.database.test_database import get_db as get_db_test
from src.main import app


@pytest.fixture
def test_client():
    app.dependency_overrides[get_db] = get_db_test

    with TestClient(app) as test_client_instance:
        yield test_client_instance

    app.dependency_overrides.clear()

def test_get_users(test_client):
    response = test_client.get("/api/v1/users")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    print(data)
