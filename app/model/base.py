import uuid as uid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import as_declarative


class CustomUUID(postgresql.UUID):
    python_type = uid.UUID


@as_declarative()
class BaseModel:
    id = Column(
        CustomUUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uid.uuid4,
    )
    created_at = Column(
        DateTime(True),
        default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


