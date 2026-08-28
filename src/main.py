from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.init_db import init_database
from src.controllers.api import api_router


# This decorator converts an asynchronous function into a context manager function
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Asynchronous context manager function for initializing the application."""

    # Startup stage
    # The code here will execute only once at startup
    init_database()

    # Pause stage
    # Here the API is already running and receiving clients' requests
    yield

    # Shutdown stage
    # The code here will execute only once at shutdown


# Initialize FastAPI application
app = FastAPI(title="Notifications System API", version="1.0.0", lifespan=lifespan)

# Controllers' routers connection
app.include_router(api_router)
