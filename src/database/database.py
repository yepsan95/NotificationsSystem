import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


# Loads variables from the .env file to Python's memory
load_dotenv()

# Get the database credentials from the environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construct database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create database engine
db_engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True # Tests connection before using it, reconnects automatically if the connection is lost
)

# Session maker configuration
SessionLocal = sessionmaker(
    autocommit=False, # Disables autocommit, enforces the use of db.commit() explicitly 
    autoflush=False, # Forbids SQLAlchemy from sending updates to the database before you do it
    bind=db_engine # Binds the session maker with the database engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
