"""Integration tests for the /movies API routes.

Uses the isolated in-memory SQLite database provided by the `client` /
`db_session` fixtures (tests/conftest.py) instead of the development
movies.db, so tests can freely create/update/delete data.
"""
from app.models.movie import Movie


def make_movie_payload(**overrides):
    payload = {
        "title": "Movie 1",
        "year": 2000,
        "studios": ["Studio"],
        "producers": ["Producer A"],
        "winner": False,
    }
    payload.update(overrides)
    return payload


def test_create_movie_returns_201(client):
    response = client.post("/movies/", json=make_movie_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Movie 1"
    assert body["id"] is not None


def test_create_movie_with_invalid_payload_returns_422(client):
    invalid_payload = {
        "title": "Missing required fields",
    }

    response = client.post("/movies/", json=invalid_payload)

    assert response.status_code == 422


def test_list_movies_returns_200(client):
    client.post("/movies/", json=make_movie_payload(title="Movie 1"))
    client.post("/movies/", json=make_movie_payload(title="Movie 2"))

    response = client.get("/movies/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_movie_by_id_returns_200(client):
    created = client.post("/movies/", json=make_movie_payload()).json()

    response = client.get(f"/movies/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_movie_by_id_not_found_returns_404(client):
    response = client.get("/movies/999")

    assert response.status_code == 404


def test_update_movie_put_returns_200(client):
    created = client.post("/movies/", json=make_movie_payload()).json()

    response = client.put(
        f"/movies/{created['id']}",
        json=make_movie_payload(title="Updated Title", winner=True),
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["winner"] is True


def test_update_movie_put_not_found_returns_404(client):
    response = client.put("/movies/999", json=make_movie_payload())

    assert response.status_code == 404


def test_patch_movie_returns_200(client):
    created = client.post("/movies/", json=make_movie_payload()).json()

    response = client.patch(
        f"/movies/{created['id']}",
        json={"winner": True},
    )

    assert response.status_code == 200
    assert response.json()["winner"] is True
    assert response.json()["title"] == created["title"]


def test_patch_movie_not_found_returns_404(client):
    response = client.patch("/movies/999", json={"winner": True})

    assert response.status_code == 404


def test_delete_movie_returns_204(client):
    created = client.post("/movies/", json=make_movie_payload()).json()

    response = client.delete(f"/movies/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/movies/{created['id']}").status_code == 404


def test_delete_movie_not_found_returns_404(client):
    response = client.delete("/movies/999")

    assert response.status_code == 404


def test_producer_awards_endpoint_returns_200_with_calculated_intervals(
    client, db_session
):
    db_session.add_all(
        [
            Movie(
                title="Movie 1",
                year=2000,
                studios=["Studio"],
                producers=["Producer A"],
                winner=True,
            ),
            Movie(
                title="Movie 2",
                year=2001,
                studios=["Studio"],
                producers=["Producer A"],
                winner=True,
            ),
            Movie(
                title="Movie 3",
                year=1999,
                studios=["Studio"],
                producers=["Producer B"],
                winner=False,
            ),
        ]
    )
    db_session.commit()

    response = client.get("/movies/producers/awards")

    assert response.status_code == 200
    assert response.json() == {
        "min": [
            {
                "producer": "Producer A",
                "interval": 1,
                "previousWin": 2000,
                "followingWin": 2001,
            }
        ],
        "max": [
            {
                "producer": "Producer A",
                "interval": 1,
                "previousWin": 2000,
                "followingWin": 2001,
            }
        ],
    }
