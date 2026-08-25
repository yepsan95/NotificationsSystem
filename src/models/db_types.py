from datetime import datetime
from typing import Annotated
import uuid
from sqlalchemy import func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Column Types for PostgreSQL
id_pk = Annotated[
    uuid.UUID,  # Native Python UUID type
    mapped_column(
        UUID(as_uuid=True),  # Specific UUID type for PostgreSQL
        primary_key=True,  # Defines id as primary key
        index=True,  # Creates index
        server_default=text(
            "gen_random_uuid()"
        ),  # Default PostgreSQL native function to generate UUID in case the application fails to generate it
    ),
]
timestamp_created = Annotated[
    datetime,  # Native Python datetime type
    mapped_column(
        server_default=func.now(),  # Default PostgreSQL native function to generate timestamp in case the application fails to generate it on creation
        nullable=False,  # Makes it non nullable
    ),
]
timestamp_updated = Annotated[
    datetime,  # Native Python datetime type
    mapped_column(
        server_default=func.now(),  # Default PostgreSQL native function to generate timestamp in case the application fails to generate it on creation
        onupdate=func.now(),  # Default PostgreSQL native function to generate timestamp in case the application fails to generate it on update
        nullable=False,  # Makes it non nullable
    ),
]
