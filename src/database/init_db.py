import sys
from sqlalchemy_utils import database_exists, create_database
from src.database.real_database import db_engine, REAL_DATABASE_URL
from src.models.base_model import Base
from src.models.user_model import User


def init_database():
    """Create physical PostgreSQL database and tables if they don't exist."""

    current_url = None
    current_engine = None
    is_running_tests = "pytest" in sys.modules

    if is_running_tests:
        from tests.database.test_database import (
            db_engine as test_db_engine,
            TEST_DATABASE_URL,
        )

        current_url = TEST_DATABASE_URL
        current_engine = test_db_engine
        print("[TEST] Initializing test database...")
    else:
        current_url = REAL_DATABASE_URL
        current_engine = db_engine
        print("[DEV/PROD] Initializing real database...")

    try:
        if not database_exists(current_url):
            print("Creating physical database with SQLAlchemy-Utils")
            create_database(current_url)

        print("Creating tables based on SQLAlchemy models")
        Base.metadata.create_all(bind=current_engine)

    except Exception as e:
        print(f"Error during database initialization: {e}")
        raise e
