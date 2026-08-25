import pytest
import uuid
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
def sample_single_user(db_session):
    """Fixture that creates a single sample user before the test."""

    user_data = {
        "first_name": "Linus",
        "middle_name": "Benedict",
        "last_name": "Torvalds",
        "email": "linus@linuxfoundation.org",
    }
    user_password = "ILoveTux"

    hashed_password = password_context.hash(user_password)

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
        | {"password_hash": password_context.hash(user["password"])}
        for user in users_data
    ]

    new_users = [User(**data) for data in users_data]

    users_data = [
        {k: v for k, v in user.items() if k != "password_hash"} for user in users_data
    ]

    db_session.add_all(new_users)
    db_session.commit()

    return users_data


def test_get_multi_users_returns_success_and_empty_list(test_http_client):
    """
    Tests GET /users endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns an empty list.
    """

    response = test_http_client.get("/api/v1/users")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == []


def test_get_multi_users_returns_success_and_one_item(
    test_http_client, sample_single_user
):
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
    assert len(data) == 1

    user_data = data[0]
    assert all(
        user_data.get(k) == v
        for k, v in sample_single_user.get_safe_attributes().items()
    )


def test_get_multi_users_returns_success_and_multiple_items(
    test_http_client, sample_multiple_users
):
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
    assert len(users_data) == len(sample_users_data)
    assert all(
        all(user.get(k) == v for k, v in sample_multiple_users[index].items())
        for index, user in enumerate(users_data)
    )


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
    assert len(paginated_users_data) == limit

    paginated_sample_users = sample_multiple_users[offset : offset + limit]
    assert all(
        all(user.get(k) == v for k, v in paginated_sample_users[index].items())
        for index, user in enumerate(paginated_users_data)
    )


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


def test_get_user_by_id_returns_success_and_one_item(
    test_http_client, sample_single_user
):
    """
    Tests GET /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns user with correct id.
    - validate user's fields.
    """

    sample_user_dict = sample_single_user.get_safe_attributes()
    user_id = sample_user_dict["id"]

    response = test_http_client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK

    user_data = response.json()
    assert user_data["id"] == user_id

    assert all(user_data.get(k) == v for k, v in sample_user_dict.items())


def test_get_user_by_id_returns_failure_when_user_does_not_exist(test_http_client):
    """
    Tests GET /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 404 when user with requested id does not exist.
    """

    user_id = str(uuid.uuid4())
    response = test_http_client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_user_returns_success_and_one_item_with_optional_fields(
    test_http_client,
):
    """
    Tests POST /users endpoint.
    Asserts:
    - response includes HTTP status code 201 when payload includes optional fields.
    - response returns created user.
    - validate created user's fields.
    """

    new_user_payload = {
        "first_name": "Linus",
        "middle_name": "Benedict",
        "last_name": "Torvalds",
        "email": "linus@linuxfoundation.org",
        "password": "ILoveTux",
    }

    response = test_http_client.post("/api/v1/users", json=new_user_payload)
    assert response.status_code == status.HTTP_201_CREATED

    user_data = response.json()
    del new_user_payload["password"]
    assert all(user_data.get(k) == v for k, v in new_user_payload.items())


def test_create_user_returns_success_and_one_item_with_required_fields(
    test_http_client,
):
    """
    Tests POST /users endpoint.
    Asserts:
    - response includes HTTP status code 201 when payload includes only required fields.
    - response returns created user.
    - validate created user's fields.
    """

    new_user_payload = {
        "first_name": "Linus",
        "middle_name": None,
        "last_name": "Torvalds",
        "email": "linus@linuxfoundation.org",
        "password": "ILoveTux",
    }

    response = test_http_client.post("/api/v1/users", json=new_user_payload)
    assert response.status_code == status.HTTP_201_CREATED

    user_data = response.json()
    del new_user_payload["password"]
    assert all(user_data.get(k) == v for k, v in new_user_payload.items())


def test_create_user_returns_failure_when_missing_required_fields(test_http_client):
    """
    Tests POST /users endpoint.
    Asserts:
    - response includes HTTP status code 422 when payload is missing required fields.
    """

    new_user_payload = {
        "first_name": "Linus",
        "last_name": "Torvalds",
        "password": "ILoveTux",
    }

    response = test_http_client.post("/api/v1/users", json=new_user_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_user_returns_success_and_one_item_with_trailing_whitespaces(
    test_http_client,
):
    """
    Tests POST /users endpoint.
    Asserts:
    - response includes HTTP status code 201 when payload includes fields with trailing whitespaces.
    - response returns created user.
    - validate created user's fields.
    """

    new_user_payload = {
        "first_name": "    Linus    ",
        "middle_name": "    Benedict    ",
        "last_name": "    Torvalds    ",
        "email": "    linus@linuxfoundation.org    ",
        "password": "    ILoveTux    ",
    }

    response = test_http_client.post("/api/v1/users", json=new_user_payload)
    assert response.status_code == status.HTTP_201_CREATED

    user_data = response.json()
    new_user_payload = {k: v.strip() for k, v in new_user_payload.items()}
    del new_user_payload["password"]
    assert all(user_data.get(k) == v for k, v in new_user_payload.items())


def test_create_user_returns_failure_when_email_already_exists(
    test_http_client, sample_single_user
):
    """
    Tests POST /users endpoint.
    Asserts:
    - response includes HTTP status code 409 when email already exists in the database.
    """

    new_user_payload = {
        "first_name": "Linus",
        "middle_name": "Tech",
        "last_name": "Tips",
        "email": "linus@linuxfoundation.org",
        "password": "ILoveNCIX",
    }

    response = test_http_client.post("/api/v1/users", json=new_user_payload)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_user_returns_failure_when_email_has_invalid_format(test_http_client):
    """
    Tests POST /users endpoint.
    Asserts:
    - response includes HTTP status code 422 when email has invalid format.
    """

    new_user_payload = {
        "first_name": "Linus",
        "last_name": "Torvalds",
        "email": "linus(at)linuxfoundation.org",
        "password": "ILoveTux",
    }

    response = test_http_client.post("/api/v1/users", json=new_user_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_user_returns_failure_when_password_has_invalid_format(
    test_http_client, db_session
):
    """
    Tests POST /users endpoint.
    Asserts:
    - response includes HTTP status code 422 when password is too short, i.e. less than 6 characters.
    - response includes HTTP status code 422 when password is too long, i.e. greater than 16 characters.
    - validate none of the users with invalid password format were created.
    """

    new_user_a_payload = {
        "first_name": "Linus",
        "middle_name": "Benedict",
        "last_name": "Torvalds",
        "email": "linus@linuxfoundation.org",
        "password": "Linux",
    }

    response_a = test_http_client.post("/api/v1/users", json=new_user_a_payload)
    assert response_a.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    new_user_b_payload = (
        {
            "first_name": "Richard",
            "middle_name": "Matthew",
            "last_name": "Stallman",
            "email": "rms@gnu.org",
            "password": "I'd just like to interject for a moment. What you're refering to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux.",
        },
    )

    response_b = test_http_client.post("/api/v1/users", json=new_user_b_payload)
    assert response_b.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    users_in_database = db_session.query(User).limit(5).all()
    assert users_in_database == []


def test_create_user_returns_failure_when_fields_have_incorrect_data_types(
    test_http_client,
):
    """
    Tests POST /users endpoint.
    Asserts:
    - response includes HTTP status code 422 when payload includes fields with incorrect data types.
    """

    new_user_payload = {
        "first_name": ["Linus"],
        "middle_name": 98,
        "last_name": "Torvalds",
        "email": "linus@linuxfoundation.org",
        "password": ("ILoveTux",),
    }

    response = test_http_client.post("/api/v1/users", json=new_user_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_replace_user_returns_success_and_replaced_item_with_optional_fields(
    test_http_client, sample_single_user
):
    """
    Tests PUT /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns replaced user.
    - validate replaced user's fields.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    replace_user_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": "FREEdom",
    }

    response = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_payload
    )
    assert response.status_code == status.HTTP_200_OK

    replaced_user_data = response.json()
    assert replaced_user_data["id"] == user_id

    del replace_user_payload["password"]
    assert all(replaced_user_data.get(k) == v for k, v in replace_user_payload.items())


def test_replace_user_returns_success_and_replaced_item_with_required_fields(
    test_http_client, sample_single_user
):
    """
    Tests PUT /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns replaced user.
    - validate replaced user's fields.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    replace_user_payload = {
        "first_name": "Richard",
        "middle_name": None,
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": "FREEdom",
    }

    response = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_payload
    )
    assert response.status_code == status.HTTP_200_OK

    replaced_user_data = response.json()
    assert replaced_user_data["id"] == user_id

    del replace_user_payload["password"]
    assert all(replaced_user_data.get(k) == v for k, v in replace_user_payload.items())


def test_replace_user_idempotency_check(test_http_client, sample_single_user):
    """
    Tests PUT /users/{user_id} endpoint.
    Asserts:
    - first response includes HTTP status code 200.
    - second response includes HTTP status code 200.
    - first and second responses are identical.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    replace_user_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": "FREEdom",
    }

    response_a = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_payload
    )
    assert response_a.status_code == status.HTTP_200_OK

    response_b = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_payload
    )
    assert response_b.status_code == status.HTTP_200_OK

    replaced_user_data_a = response_a.json()
    replaced_user_data_b = response_b.json()

    del replaced_user_data_a["updated_at"]
    del replaced_user_data_b["updated_at"]

    assert replaced_user_data_a == replaced_user_data_b


def test_replace_user_returns_failure_when_missing_required_fields(
    test_http_client, sample_single_user
):
    """
    Tests PUT /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 422 when payload is missing required fields.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    replace_user_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "password": "FREEdom",
    }

    response = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_payload
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_replace_user_returns_success_and_replaced_item_with_trailing_whitespaces(
    test_http_client, sample_single_user
):
    """
    Tests PUT /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 200 when payload includes fields with trailing whitespaces.
    - response returns replaced user.
    - validate replaced user's fields.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    replace_user_payload = {
        "first_name": "    Richard    ",
        "middle_name": "    Matthew    ",
        "last_name": "    Stallman    ",
        "email": "    rms@gnu.org    ",
        "password": "    FREEdom    ",
    }

    response = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_payload
    )
    assert response.status_code == status.HTTP_200_OK

    replaced_user_data = response.json()
    assert replaced_user_data["id"] == user_id

    replace_user_payload = {k: v.strip() for k, v in replace_user_payload.items()}
    del replace_user_payload["password"]
    assert all(replaced_user_data.get(k) == v for k, v in replace_user_payload.items())


def test_replace_user_returns_failure_when_email_already_exists(
    test_http_client, sample_single_user, db_session
):
    """
    Tests PUT /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 409 when email already exists in the database.
    """

    new_user_data = {
        "first_name": "Rick",
        "middle_name": "Matt",
        "last_name": "Stally",
        "email": "rms@gnu.org",
        "password": "OpenSource",
    }
    hashed_password = password_context.hash(new_user_data["password"])
    new_user_data.pop("password", None)
    new_user = User(**new_user_data, password_hash=hashed_password)
    db_session.add(new_user)
    db_session.commit()

    user_id = sample_single_user.get_safe_attributes()["id"]

    replace_user_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": "FREEdom",
    }

    response = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_payload
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_replace_user_returns_failure_when_email_has_invalid_format(
    test_http_client, sample_single_user
):
    """
    Tests PUT /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 422 when email has invalid format.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    replace_user_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms(at)gnu.org",
        "password": "FREEdom",
    }

    response = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_payload
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_replace_user_returns_failure_when_password_has_invalid_format(
    test_http_client, sample_single_user, db_session
):
    """
    Tests PUT /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 422 when password is too short, i.e. less than 6 characters.
    - response includes HTTP status code 422 when password is too long, i.e. greater than 16 characters.
    - validate none of the users with invalid password format were replaced.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    replace_user_a_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": "GNU",
    }

    response_a = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_a_payload
    )
    assert response_a.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    replace_user_b_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": "I'd just like to interject for a moment. What you're refering to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux.",
    }

    response_b = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_b_payload
    )
    assert response_b.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    original_updated_at = sample_single_user.get_safe_attributes()["updated_at"]
    original_user = db_session.get(User, user_id)
    assert original_updated_at == original_user.updated_at.isoformat()


def test_replace_user_returns_failure_when_fields_have_incorrect_data_types(
    test_http_client, sample_single_user
):
    """
    Tests PUT /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 422 when payload includes fields with incorrect data types.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    replace_user_payload = {
        "first_name": ["Richard"],
        "middle_name": 77,
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": ("FREEdom",),
    }

    response = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_payload
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_replace_user_returns_failure_when_user_does_not_exist(
    test_http_client, sample_single_user
):
    """
    Tests PUT /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 404 when user does not exist.
    """

    user_id = str(uuid.uuid4())

    replace_user_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": "FREEdom",
    }

    response = test_http_client.put(
        f"/api/v1/users/{user_id}", json=replace_user_payload
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user_returns_success_and_updated_item_with_one_field(
    test_http_client, sample_single_user
):
    """
    Tests PATCH /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns updated user.
    - validate updated user's fields.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    update_user_payload = {"first_name": "Freax"}

    response = test_http_client.patch(
        f"/api/v1/users/{user_id}", json=update_user_payload
    )
    assert response.status_code == status.HTTP_200_OK

    updated_user_data = response.json()
    assert updated_user_data["id"] == user_id

    assert all(updated_user_data.get(k) == v for k, v in update_user_payload.items())


def test_update_user_returns_success_and_updated_item_with_multiple_fields(
    test_http_client, sample_single_user
):
    """
    Tests PATCH /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns updated user.
    - validate updated user's fields.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    update_user_payload = {
        "first_name": "Guido",
        "middle_name": "Van",
        "last_name": "Rossum",
        "email": "guido@python.org",
        "password": "ZenOfPython",
    }

    response = test_http_client.patch(
        f"/api/v1/users/{user_id}", json=update_user_payload
    )
    assert response.status_code == status.HTTP_200_OK

    updated_user_data = response.json()
    assert updated_user_data["id"] == user_id

    del update_user_payload["password"]
    assert all(updated_user_data.get(k) == v for k, v in update_user_payload.items())


def test_update_user_returns_success_and_updated_item_with_empty_payload(
    test_http_client, sample_single_user
):
    """
    Tests PATCH /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns updated user.
    - validate updated user's fields.
    """

    original_sample_user = sample_single_user.get_safe_attributes()
    user_id = original_sample_user["id"]
    del original_sample_user["updated_at"]

    update_user_payload = {}

    response = test_http_client.patch(
        f"/api/v1/users/{user_id}", json=update_user_payload
    )
    assert response.status_code == status.HTTP_200_OK

    updated_user_data = response.json()
    assert updated_user_data["id"] == user_id

    assert all(updated_user_data.get(k) == v for k, v in original_sample_user.items())


def test_update_user_returns_success_and_updated_item_with_same_values(
    test_http_client, sample_single_user
):
    """
    Tests PATCH /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns updated user.
    - validate updated user's fields.
    """

    original_sample_user = sample_single_user.get_safe_attributes()
    user_id = original_sample_user["id"]
    del original_sample_user["id"]
    del original_sample_user["created_at"]
    del original_sample_user["updated_at"]

    update_user_payload = {**original_sample_user}

    response = test_http_client.patch(
        f"/api/v1/users/{user_id}", json=update_user_payload
    )
    assert response.status_code == status.HTTP_200_OK

    updated_user_data = response.json()
    assert updated_user_data["id"] == user_id

    assert all(updated_user_data.get(k) == v for k, v in original_sample_user.items())


def test_update_user_returns_success_and_updated_item_with_trailing_whitespaces(
    test_http_client, sample_single_user
):
    """
    Tests PATCH /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 200 when payload includes fields with trailing whitespaces.
    - response returns updated user.
    - validate updated user's fields.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    update_user_payload = {
        "first_name": "    Richard    ",
        "middle_name": "    Matthew    ",
        "last_name": "    Stallman    ",
        "email": "    rms@gnu.org    ",
        "password": "    FREEdom    ",
    }

    response = test_http_client.patch(
        f"/api/v1/users/{user_id}", json=update_user_payload
    )
    assert response.status_code == status.HTTP_200_OK

    updated_user_data = response.json()
    assert updated_user_data["id"] == user_id

    update_user_payload = {k: v.strip() for k, v in update_user_payload.items()}
    del update_user_payload["password"]
    assert all(updated_user_data.get(k) == v for k, v in update_user_payload.items())


def test_update_user_returns_failure_when_email_already_exists(
    test_http_client, sample_single_user, db_session
):
    """
    Tests PATCH /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 409 when email already exists in the database.
    """

    new_user_data = {
        "first_name": "Rick",
        "middle_name": "Matt",
        "last_name": "Stally",
        "email": "rms@gnu.org",
        "password": "OpenSource",
    }
    hashed_password = password_context.hash(new_user_data["password"])
    new_user_data.pop("password", None)
    new_user = User(**new_user_data, password_hash=hashed_password)
    db_session.add(new_user)
    db_session.commit()

    user_id = sample_single_user.get_safe_attributes()["id"]

    update_user_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": "FREEdom",
    }

    response = test_http_client.patch(
        f"/api/v1/users/{user_id}", json=update_user_payload
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_user_returns_failure_when_email_has_invalid_format(
    test_http_client, sample_single_user
):
    """
    Tests PATCH /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 422 when email has invalid format.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    update_user_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms(at)gnu.org",
        "password": "FREEdom",
    }

    response = test_http_client.patch(
        f"/api/v1/users/{user_id}", json=update_user_payload
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_update_user_returns_failure_when_password_has_invalid_format(
    test_http_client, sample_single_user, db_session
):
    """
    Tests PATCH /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 422 when password is too short, i.e. less than 6 characters.
    - response includes HTTP status code 422 when password is too long, i.e. greater than 16 characters.
    - validate none of the users with invalid password format were updated.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    update_user_a_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": "GNU",
    }

    response_a = test_http_client.put(
        f"/api/v1/users/{user_id}", json=update_user_a_payload
    )
    assert response_a.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    update_user_b_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": "I'd just like to interject for a moment. What you're refering to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux.",
    }

    response_b = test_http_client.put(
        f"/api/v1/users/{user_id}", json=update_user_b_payload
    )
    assert response_b.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    original_updated_at = sample_single_user.get_safe_attributes()["updated_at"]
    original_user = db_session.get(User, user_id)
    assert original_updated_at == original_user.updated_at.isoformat()


def test_update_user_returns_failure_when_fields_have_incorrect_data_types(
    test_http_client, sample_single_user
):
    """
    Tests PATCH /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 422 when payload includes fields with incorrect data types.
    """

    user_id = sample_single_user.get_safe_attributes()["id"]

    update_user_payload = {
        "first_name": ["Richard"],
        "middle_name": 77,
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": ("FREEdom",),
    }

    response = test_http_client.put(
        f"/api/v1/users/{user_id}", json=update_user_payload
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_update_user_returns_failure_when_user_does_not_exist(
    test_http_client, sample_single_user
):
    """
    Tests PATCH /users/{user_id} endpoint.
    Asserts:
    - response includes HTTP status code 404 when user does not exist.
    """

    user_id = str(uuid.uuid4())

    update_user_payload = {
        "first_name": "Richard",
        "middle_name": "Matthew",
        "last_name": "Stallman",
        "email": "rms@gnu.org",
        "password": "FREEdom",
    }

    response = test_http_client.put(
        f"/api/v1/users/{user_id}", json=update_user_payload
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
