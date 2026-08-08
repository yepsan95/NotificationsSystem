import pytest
from fastapi import status
from fastapi.testclient import TestClient
from src.models.base_model import Base
from src.models.user_model import User
from src.services.user_service import password_context
from src.database.real_database import get_db
from tests.database.test_database import get_db as get_db_test
from src.main import app


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_suite():
    """Fixture wrapper for the entire test suite execution."""

    # Before All stage
    # The code here will execute once before all tests

    print("\n[Before All] Starting container and test database...")

    yield

    # After All stage
    # The code here will execute once after all tests

    print("\n[After All] Destroying test database and cleaning containers...")

    return "Setup and teardown test suite fixture generator terminated."


@pytest.fixture(scope="function")
def db_session():
    """Fixture for test database session."""

    db_generator = get_db_test()
    db = next(db_generator)

    try:
        yield db
    finally:
        print("\n[After Each] Deleting database data...")

        try:
            for db_table in reversed(Base.metadata.sorted_tables):
                db.execute(db_table.delete())
            db.commit()
        except Exception as e:
            print(f"Error clearing database tables: {e}")
            db.rollback()

        try:
            next(db_generator)
        except StopIteration as e:
            pass


@pytest.fixture(scope="function")
def test_http_client():
    """Fixture for test HTTP client."""

    # Before Each stage
    # The code here will execute before each test

    print("\n[Before Each] Overriding dependencies and preparing test state...")

    app.dependency_overrides[get_db] = get_db_test

    with TestClient(app) as test_http_client_instance:
        yield test_http_client_instance

    # After Each stage
    # The code here will execute after each test

    print("\n[After Each] Cleaning dependency overrides and restoring database state...")

    app.dependency_overrides.clear()


@pytest.fixture
def sample_single_user(db_session):
    """Creates a single user before the test."""

    user_data = {
        "first_name": "Linus",
        "middle_name": "Benedict",
        "last_name": "Torvalds",
        "email": "linus@linuxfoundation.org"
    }
    user_password = "ILoveTux"

    hashed_password = password_context.hash(user_password)

    new_user = User(**user_data, password_hash=hashed_password)

    db_session.add(new_user)
    db_session.commit()

    return user_data


def test_get_multi_users_returns_success_status(test_http_client):
    """Tests GET /users endpoint returns HTTP status code 200."""

    response = test_http_client.get("/api/v1/users")
    assert response.status_code == status.HTTP_200_OK


def test_get_multi_users_returns_one_item(test_http_client, sample_single_user):
    """Tests GET /users endpoint returns a single item."""

    response = test_http_client.get("/api/v1/users")
    data = response.json()
    assert (len(data) == 1)


def test_get_multi_users_returns_valid_user_fields(test_http_client, sample_single_user):
    """Tests GET /users endpoint returns an item and checks all fields."""

    response = test_http_client.get("/api/v1/users")
    data = response.json()
    assert (len(data) == 1)
    user_data = data[0]

    assert all(user_data.get(k) == v for k, v in sample_single_user.items())
