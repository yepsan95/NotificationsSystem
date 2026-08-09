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
    """Fixture that creates a single sample user before the test."""

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


@pytest.fixture
def sample_multiple_users(db_session):
    """Fixture that creates multiple sample users before the test."""

    users_data = [
        {
            "first_name": "Linus",
            "middle_name": "Benedict",
            "last_name": "Torvalds",
            "email": "linus@linuxfoundation.org",
            "password": "ILoveTux"
        },
        {
            "first_name": "Richard",
            "middle_name": "Matthew",
            "last_name": "Stallman",
            "email": "rms@gnu.org",
            "password": "FREEdom"
        },
        {
            "first_name": "Guido",
            "middle_name": "Van",
            "last_name": "Rossum",
            "email": "guido@python.org",
            "password": "ZenOfPython"
        },
        {
            "first_name": "Tim",
            "middle_name": "John",
            "last_name": "Berners-Lee",
            "email": "timbl@w3.org",
            "password": "Web3IsAwesome"
        },
        {
            "first_name": "Miller",
            "middle_name": "Puckette",
            "last_name": "Smith",
            "email": "msp@ucsd.edu",
            "password": "Pd>>Max"
        },
        {
            "first_name": "Dennis",
            "middle_name": "MacAlistair",
            "last_name": "Ritchie",
            "email": "dmr@bell-labs.com",
            "password": "CAndUnix1972"
        },
        {
            "first_name": "Ken",
            "middle_name": "Lane",
            "last_name": "Thompson",
            "email": "ken@google.com",
            "password": "GoAndB311Labs"
        },
        {
            "first_name": "Brian",
            "middle_name": "Wilson",
            "last_name": "Kernighan",
            "email": "bwk@cs.princeton.edu",
            "password": "AWKandTheCBook"
        },
        {
            "first_name": "Yukihiro",
            "middle_name": "",
            "last_name": "Matsumoto",
            "email": "matz@ruby-lang.org",
            "password": "MatzIsNiceAndSoAreWe"
        },
        {
            "first_name": "Bram",
            "middle_name": "",
            "last_name": "Moolenaar",
            "email": "bram@vim.org",
            "password": "HelpUgandaVim"
        },
        {
            "first_name": "Daniel",
            "middle_name": "",
            "last_name": "Stenberg",
            "email": "daniel@haxx.se",
            "password": "cURLTheWorld"
        },
        {
            "first_name": "Mitchell",
            "middle_name": "",
            "last_name": "Hashimoto",
            "email": "mitchell@hashicorp.com",
            "password": "VagrantToTerraform"
        },
        {
            "first_name": "Graydon",
            "middle_name": "",
            "last_name": "Hoare",
            "email": "graydon@pobox.com",
            "password": "RustSafetyFirst"
        },
        {
            "first_name": "Rasmus",
            "middle_name": "",
            "last_name": "Lerdorf",
            "email": "rasmus@php.net",
            "password": "PersonalHomePage"
        },
        {
            "first_name": "Ian",
            "middle_name": "Murdock",
            "last_name": "Debian",
            "email": "ian@debian.org",
            "password": "IanAndDebra1993"
        },
        {
            "first_name": "Miguel",
            "middle_name": "",
            "last_name": "de Icaza",
            "email": "miguel@gnome.org",
            "password": "GnomeAndMono"
        },
        {
            "first_name": "Michael",
            "middle_name": "",
            "last_name": "Widenius",
            "email": "monty@mariadb.org",
            "password": "MontyMySQLMariaDB"
        },
        {
            "first_name": "Fabrice",
            "middle_name": "",
            "last_name": "Bellard",
            "email": "fabrice@bellard.org",
            "password": "QEMUandFFmpeg"
        },
        {
            "first_name": "Theo",
            "middle_name": "de",
            "last_name": "Raadt",
            "email": "deraadt@openbsd.org",
            "password": "OpenBSDOpenSSH"
        },
        {
            "first_name": "Andrew",
            "middle_name": "",
            "last_name": "Tridgell",
            "email": "tridge@samba.org",
            "password": "SambaAndRsync"
        }
    ]

    users_data = [{k: v for k, v in user.items() if k != "password"} | {"password_hash": password_context.hash(user["password"])} for user in users_data]

    new_users = [User(**data) for data in users_data]
    
    users_data = [{k: v for k, v in user.items() if k != "password_hash"} for user in users_data]

    db_session.add_all(new_users)
    db_session.commit()

    return users_data


def test_get_multi_users_returns_success_status_and_empty_list(test_http_client):
    """
    Tests GET /users endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns an empty list.
    """

    response = test_http_client.get("/api/v1/users")
    assert response.status_code == status.HTTP_200_OK


def test_get_multi_users_returns_success_status_and_one_item(test_http_client, sample_single_user):
    """
    Tests GET /users endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns a list with one user.
    - validate user's fields.
    """

    response = test_http_client.get("/api/v1/users")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert (len(data) == 1)

    user_data = data[0]
    assert all(user_data.get(k) == v for k, v in sample_single_user.items())


def test_get_multi_users_returns_success_status_and_multiple_items(test_http_client, sample_multiple_users):
    """
    Tests GET /users endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns a list with default limit of 10 users.
    - validate users' fields.
    """

    response = test_http_client.get("/api/v1/users")
    assert response.status_code == status.HTTP_200_OK

    users_data = response.json()
    sample_users_data = sample_multiple_users[:10]
    assert (len(users_data) == len(sample_users_data))
    assert all(all(user.get(k) == v for k, v in sample_multiple_users[index].items()) for index, user in enumerate(users_data))


def test_get_multi_users_pagination(test_http_client, sample_multiple_users):
    """
    Tests GET /users endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns a list with a limit of 5 users.
    - response returns a list with an offset of 10 users.
    - validate users' fields.
    """
    
    offset = 10
    limit = 5

    response = test_http_client.get("/api/v1/users", params={"offset": 10, "limit": 5})
    assert response.status_code == status.HTTP_200_OK

    paginated_users_data = response.json()
    assert (len(paginated_users_data) == limit)

    paginated_sample_users = sample_multiple_users[offset:offset + limit]
    assert all(all(user.get(k) == v for k, v in paginated_sample_users[index].items()) for index, user in enumerate(paginated_users_data))


def test_get_multi_users_filters(test_http_client, sample_multiple_users):
    """
    Tests GET /users endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns a list of users that matches the filters criteria.
    - validate users' fields.
    """

    pass


def test_get_multi_users_returns_failure_when_database_down(test_http_client):
    """
    Tests GET /users endpoint.
    Asserts:
    - response includes HTTP status code 500 when database is down.
    """

    pass
