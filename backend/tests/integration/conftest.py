import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.infrastructure.database.dependencies import get_db
from app.infrastructure.database.base import Base
from app.infrastructure.database.connection import SessionLocal


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    yield TestClient(app)

    app.dependency_overrides.clear()


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
