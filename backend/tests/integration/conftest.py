import pytest

from app.infrastructure.database.base import Base
from app.infrastructure.database.connection import SessionLocal


@pytest.fixture
def db_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()

        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())

        session.commit()
        session.close()
