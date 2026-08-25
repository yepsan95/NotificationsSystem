import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from src.database.base_database import BaseDatabaseClient


class TestDatabaseClient(BaseDatabaseClient):
    """Test database client class. This client will be used exclusively for testing."""

    def __init__(self, database_url: str, container_names=[]):
        parsed_url = urlparse(database_url)
        hostname = parsed_url.hostname
        actual_db_name = parsed_url.path.lstrip("/")

        # Check if the database is running in a Docker container
        # If app is is running in localhost and the database in a Docker container,
        # the database hostname will be 'localhost' or '127.0.0.1'.
        # If both the app and the database are running in separate Docker containers,
        # the database hostname will be the name of the container.

        is_localhost = hostname in ["localhost", "127.0.0.1"]
        is_docker_container = hostname in [*container_names, "0.0.0.0"]
        has_test_keyword = "test" in actual_db_name.lower()

        if not (is_localhost or is_docker_container) or not has_test_keyword:
            raise ValueError(
                f"CRITICAL DATABASE SAFETY VIOLATION:"
                f"{self.current_class_name} was attempted to initialize during a test suite run with a non-test database URL."
                f"Execution halted."
            )

        super().__init__(database_url, container_names)


# Loads variables from the .env file to Python's memory
load_dotenv(".env")

# Get the database credentials from the environment variables
TEST_DB_DOCKER_CONTAINER = os.getenv("TEST_DB_DOCKER_CONTAINER")
TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_PORT = os.getenv("TEST_DB_PORT")
TEST_DB_NAME = os.getenv("TEST_DB_NAME")

# Construct database URL
TEST_DATABASE_URL = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"

# Instatiate database client
test_client = TestDatabaseClient(TEST_DATABASE_URL, [TEST_DB_DOCKER_CONTAINER])

# Store database engine
db_engine = test_client.engine

# Store session maker configuration
SessionLocal = test_client.SessionLocal

# Store function to get database client session
get_db = test_client.get_db
