"""Tests for the application startup behavior (app/main.py lifespan).

Covers: empty database -> CSV is imported; already-populated database ->
CSV import is skipped and records are not duplicated. Uses an isolated
in-memory SQLite database, monkeypatching `app.database.engine`/
`SessionLocal` so the lifespan (which reads those at call time) never
touches the real movies.db.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import database
from app.main import app
from app.models.movie import Movie
from scripts.import_csv import import_movies

DATASET_MOVIE_COUNT = 206


@pytest.fixture()
def isolated_database(monkeypatch):
    """Point app.database at an isolated in-memory DB with tables created.

    Tables are created here (not by the lifespan) to represent the two
    scenarios under test: an empty database and an already-populated one
    both start from an existing schema, same as a real movies.db would.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False
    )
    database.Base.metadata.create_all(bind=engine)

    monkeypatch.setattr(database, "engine", engine)
    monkeypatch.setattr(database, "SessionLocal", TestingSessionLocal)

    yield TestingSessionLocal

    database.Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_startup_imports_csv_when_database_is_empty(isolated_database):
    with TestClient(app) as client:
        movies_response = client.get("/movies/")
        assert movies_response.status_code == 200
        assert len(movies_response.json()) == DATASET_MOVIE_COUNT

        awards_response = client.get("/movies/producers/awards")
        assert awards_response.status_code == 200
        assert awards_response.json() == {
            "min": [
                {
                    "producer": "Joel Silver",
                    "interval": 1,
                    "previousWin": 1990,
                    "followingWin": 1991,
                }
            ],
            "max": [
                {
                    "producer": "Matthew Vaughn",
                    "interval": 13,
                    "previousWin": 2002,
                    "followingWin": 2015,
                }
            ],
        }


def test_startup_skips_import_when_database_already_has_movies(
    isolated_database,
):
    seed_session = isolated_database()
    seed_session.add(
        Movie(
            title="Existing Movie",
            year=2020,
            studios=["Studio"],
            producers=["Producer"],
            winner=False,
        )
    )
    seed_session.commit()
    seed_session.close()

    with TestClient(app) as client:
        response = client.get("/movies/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Existing Movie"


def test_import_movies_does_not_duplicate_records_when_run_twice(
    isolated_database,
):
    import_movies()
    import_movies()

    session = isolated_database()
    try:
        count = session.query(Movie).count()
    finally:
        session.close()

    assert count == DATASET_MOVIE_COUNT
