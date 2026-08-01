import sys
from abc import ABC
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class BaseDatabaseClient(ABC):
    """Base database client abstract class. Will be inherited by all other database clients."""

    def __init__(self, database_url: str, container_names=[]):
        self.current_class_name = self.__class__.__name__
        self.container_names = container_names
        self.is_running_tests = "pytest" in sys.modules

        parsed_url = urlparse(database_url)
        scheme = parsed_url.scheme
        username = parsed_url.username
        hostname = parsed_url.hostname
        port = parsed_url.port
        path = parsed_url.path
        actual_db_name = path.lstrip("/")

        safe_url = f"{scheme}://{username}@{hostname}:{port}{path}"
        
        self.engine = create_engine(
            database_url,
            pool_pre_ping=True
        )

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_db(self):
        # Check if the test database client is trying to access the real database by mistake
        if self.current_class_name in ["BaseDatabaseClient", "RealDatabaseClient"] and self.is_running_tests:
            raise RuntimeError(
                f"CRITICAL DATABASE SAFETY VIOLATION:"
                f"{self.current_class_name} attempted to access the real database during a test suite run."
                f"You must override this dependency using app.dependency_overrides."
                f"Execution blocked."
            )

        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
