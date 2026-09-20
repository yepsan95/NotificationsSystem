import pytest
from fastapi.testclient import TestClient

from src.core.security import hash_password
from src.database.real_database import get_db
from src.main import app
from src.models.base_model import Base
from src.models.user_model import User
from tests.database.test_database import get_db as get_db_test


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
            raise

        try:
            next(db_generator)
        except StopIteration:
            pass


@pytest.fixture(scope="function")
def test_http_client(db_session):
    """Fixture for test HTTP client."""

    # Before Each stage
    # The code here will execute before each test

    print("\n[Before Each] Overriding dependencies and preparing test state...")

    app.dependency_overrides[get_db] = get_db_test

    with TestClient(app) as test_http_client_instance:
        yield test_http_client_instance

    # After Each stage
    # The code here will execute after each test

    for db_table in reversed(Base.metadata.sorted_tables):
        db_session.execute(db_table.delete())
    db_session.commit()

    print(
        "\n[After Each] Cleaning dependency overrides and restoring database state..."
    )

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_password():
    """Fixture that returns a sample user's password."""

    return "ILoveTux"


@pytest.fixture
def sample_single_user(db_session, sample_user_password):
    """Fixture that creates a single sample user before the test."""

    user_data = {
        "first_name": "Linus",
        "middle_name": "Benedict",
        "last_name": "Torvalds",
        "email": "linus@linuxfoundation.org",
        "phone_number": "+1234567890",
        "device_token": "mock_firebase_device_token_xyz_123",
    }
    user_password = sample_user_password

    hashed_password = hash_password(user_password)

    new_user = User(**user_data, password_hash=hashed_password)

    db_session.add(new_user)
    db_session.commit()

    return new_user


@pytest.fixture
def sample_secondary_password():
    """Fixture that returns a sample user's password."""

    return "FREEdom"


@pytest.fixture
def sample_secondary_user(db_session, sample_secondary_password):
    """Fixture that creates a single sample user before the test."""

    user_data = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "phone_number": "+9876543210",
        "device_token": "mock_firebase_device_token_abc_456",
    }
    user_password = sample_secondary_password

    hashed_password = hash_password(user_password)

    new_user = User(**user_data, password_hash=hashed_password)

    db_session.add(new_user)
    db_session.commit()

    return new_user


@pytest.fixture
def sample_multiple_users(db_session):
    """Fixture that creates multiple sample users before the test."""

    users_data = [
        {
            "first_name": "Linus",
            "middle_name": "Benedict",
            "last_name": "Torvalds",
            "email": "linus@linuxfoundation.org",
            "password": "ILoveTux",
        },
        {
            "first_name": "Richard",
            "middle_name": "Matthew",
            "last_name": "Stallman",
            "email": "rms@gnu.org",
            "password": "FREEdom",
        },
        {
            "first_name": "Guido",
            "middle_name": "Van",
            "last_name": "Rossum",
            "email": "guido@python.org",
            "password": "ZenOfPython",
        },
        {
            "first_name": "Tim",
            "middle_name": "John",
            "last_name": "Berners-Lee",
            "email": "timbl@w3.org",
            "password": "Web3IsAwesome",
        },
        {
            "first_name": "Miller",
            "middle_name": "Puckette",
            "last_name": "Smith",
            "email": "msp@ucsd.edu",
            "password": "Pd>>Max",
        },
        {
            "first_name": "Dennis",
            "middle_name": "MacAlistair",
            "last_name": "Ritchie",
            "email": "dmr@bell-labs.com",
            "password": "CAndUnix1972",
        },
        {
            "first_name": "Ken",
            "middle_name": "Lane",
            "last_name": "Thompson",
            "email": "ken@google.com",
            "password": "GoAndB311Labs",
        },
        {
            "first_name": "Brian",
            "middle_name": "Wilson",
            "last_name": "Kernighan",
            "email": "bwk@cs.princeton.edu",
            "password": "AWKandTheCBook",
        },
        {
            "first_name": "Yukihiro",
            "middle_name": "",
            "last_name": "Matsumoto",
            "email": "matz@ruby-lang.org",
            "password": "MatzIsNiceAndSoAreWe",
        },
        {
            "first_name": "Bram",
            "middle_name": "",
            "last_name": "Moolenaar",
            "email": "bram@vim.org",
            "password": "HelpUgandaVim",
        },
        {
            "first_name": "Daniel",
            "middle_name": "",
            "last_name": "Stenberg",
            "email": "daniel@haxx.se",
            "password": "cURLTheWorld",
        },
        {
            "first_name": "Mitchell",
            "middle_name": "",
            "last_name": "Hashimoto",
            "email": "mitchell@hashicorp.com",
            "password": "VagrantToTerraform",
        },
        {
            "first_name": "Graydon",
            "middle_name": "",
            "last_name": "Hoare",
            "email": "graydon@pobox.com",
            "password": "RustSafetyFirst",
        },
        {
            "first_name": "Rasmus",
            "middle_name": "",
            "last_name": "Lerdorf",
            "email": "rasmus@php.net",
            "password": "PersonalHomePage",
        },
        {
            "first_name": "Ian",
            "middle_name": "Murdock",
            "last_name": "Debian",
            "email": "ian@debian.org",
            "password": "IanAndDebra1993",
        },
        {
            "first_name": "Miguel",
            "middle_name": "",
            "last_name": "de Icaza",
            "email": "miguel@gnome.org",
            "password": "GnomeAndMono",
        },
        {
            "first_name": "Michael",
            "middle_name": "",
            "last_name": "Widenius",
            "email": "monty@mariadb.org",
            "password": "MontyMySQLMariaDB",
        },
        {
            "first_name": "Fabrice",
            "middle_name": "",
            "last_name": "Bellard",
            "email": "fabrice@bellard.org",
            "password": "QEMUandFFmpeg",
        },
        {
            "first_name": "Theo",
            "middle_name": "de",
            "last_name": "Raadt",
            "email": "deraadt@openbsd.org",
            "password": "OpenBSDOpenSSH",
        },
        {
            "first_name": "Andrew",
            "middle_name": "",
            "last_name": "Tridgell",
            "email": "tridge@samba.org",
            "password": "SambaAndRsync",
        },
    ]

    users_data = [
        {k: v for k, v in user.items() if k != "password"}
        | {"password_hash": hash_password(user["password"])}
        for user in users_data
    ]

    new_users = [User(**data) for data in users_data]

    users_data = [
        {k: v for k, v in user.items() if k != "password_hash"} for user in users_data
    ]

    db_session.add_all(new_users)
    db_session.commit()

    return users_data


@pytest.fixture
def auth_user_and_cookie(
    db_session, test_http_client, sample_single_user, sample_user_password
):
    """Fixture that logs a user in."""

    login_payload = {
        "email": sample_single_user.get_safe_attributes()["email"],
        "password": sample_user_password,
    }
    test_http_client.post("https://testserver/api/v1/auth/login", json=login_payload)

    return sample_single_user
