from app.models.movie import Movie
from app.services.producer_awards import calculate_producer_intervals


def test_calculate_producer_intervals():
    movies = [
        Movie(
            title="Movie 1",
            year=2000,
            studios=["Studio"],
            producers=["Producer A"],
            winner=True,
        ),
        Movie(
            title="Movie 2",
            year=2005,
            studios=["Studio"],
            producers=["Producer A"],
            winner=True,
        ),
        Movie(
            title="Movie 3",
            year=2018,
            studios=["Studio"],
            producers=["Producer A"],
            winner=True,
        ),
        Movie(
            title="Movie 4",
            year=2008,
            studios=["Studio"],
            producers=["Producer B"],
            winner=True,
        ),
        Movie(
            title="Movie 5",
            year=2009,
            studios=["Studio"],
            producers=["Producer B"],
            winner=True,
        ),
    ]

    result = calculate_producer_intervals(movies)

    assert [
        interval.model_dump()
        for interval in result.min
    ] == [
        {
            "producer": "Producer B",
            "interval": 1,
            "previousWin": 2008,
            "followingWin": 2009,
        }
    ]

    assert [
        interval.model_dump()
        for interval in result.max
    ] == [
        {
            "producer": "Producer A",
            "interval": 13,
            "previousWin": 2005,
            "followingWin": 2018,
        }
    ]