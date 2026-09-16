import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def db_session():
    """Isolated in-memory SQLite session, separate from movies.db."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False
    )
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(db_session: Session):
    """TestClient wired to the isolated test database via get_db override.

    Deliberately not used as a context manager (`with TestClient(app)`):
    that would trigger the app's lifespan, which creates tables and
    imports the CSV against `app.database.engine`/`SessionLocal` — i.e.
    the real movies.db, since this fixture only overrides `get_db` for
    route handlers. Startup/import behavior is covered separately in
    tests/test_startup.py, where the database module's engine/session
    are monkeypatched before the lifespan runs.
    """

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()
