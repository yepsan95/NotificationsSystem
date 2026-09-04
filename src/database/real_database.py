import os
from dotenv import load_dotenv
from src.database.base_database import BaseDatabaseClient


class RealDatabaseClient(BaseDatabaseClient):
    """Real database client class. This client will be used exclusively for development and production environments."""


# Loads variables from the .env file to Python's memory
load_dotenv(".env")

# Get the database credentials from the environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construct database URL
REAL_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Instantiate database client
real_client = RealDatabaseClient(REAL_DATABASE_URL)

# Store database engine
db_engine = real_client.engine

# Store session maker configuration
SessionLocal = real_client.SessionLocal

# Store function to get database client session
get_db = real_client.get_db
