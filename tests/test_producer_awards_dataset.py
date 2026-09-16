"""End-to-end test of the producer awards endpoint with the real dataset.

Loads data/Movielist.csv into the isolated test database (see
tests/conftest.py) and exercises FastAPI + SQLAlchemy + the interval
service together, validating the exact result expected by SPECS.md.

Expected min/max were derived independently from the CSV (see
ai/prompts/ for the record of that analysis), not by reusing
calculate_producer_intervals, to avoid a tautological assertion.
"""
import csv
from pathlib import Path

from app.models.movie import Movie
from scripts.import_csv import normalize_row

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "Movielist.csv"


def test_producer_awards_endpoint_with_real_dataset(client, db_session):
    with CSV_PATH.open(mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            movie_data = normalize_row(row)
            db_session.add(Movie(**movie_data.model_dump()))
    db_session.commit()

    response = client.get("/movies/producers/awards")

    assert response.status_code == 200
    data = response.json()

    assert data["min"] == [
        {
            "producer": "Joel Silver",
            "interval": 1,
            "previousWin": 1990,
            "followingWin": 1991,
        }
    ]
    assert data["max"] == [
        {
            "producer": "Matthew Vaughn",
            "interval": 13,
            "previousWin": 2002,
            "followingWin": 2015,
        }
    ]
