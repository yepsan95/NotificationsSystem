from sqlalchemy_utils import database_exists, create_database
from src.database.database import db_engine, DATABASE_URL
from src.models.base_model import Base
from src.models.user_model import User

def init_database():
    """Create physical PostgreSQL and tables if they don't exist."""

    try:
        if not database_exists(DATABASE_URL):
            print("Creating physical database with SQLAlchemy-Utils")
            create_database(DATABASE_URL)

        print("Creating tables based on SQLAlchemy models")
        Base.metadata.create_all(bind=db_engine)

    except Exception as e:
        print(f"Error during database initialization: {e}")
        raise e
