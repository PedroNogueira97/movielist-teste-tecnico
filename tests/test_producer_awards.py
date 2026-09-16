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


def test_tie_between_multiple_producers_in_min_and_max():
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
            year=2002,
            studios=["Studio"],
            producers=["Producer A"],
            winner=True,
        ),
        Movie(
            title="Movie 3",
            year=2010,
            studios=["Studio"],
            producers=["Producer B"],
            winner=True,
        ),
        Movie(
            title="Movie 4",
            year=2012,
            studios=["Studio"],
            producers=["Producer B"],
            winner=True,
        ),
    ]

    result = calculate_producer_intervals(movies)

    assert {interval.producer for interval in result.min} == {
        "Producer A",
        "Producer B",
    }
    assert {interval.producer for interval in result.max} == {
        "Producer A",
        "Producer B",
    }
    assert all(interval.interval == 2 for interval in result.min)
    assert all(interval.interval == 2 for interval in result.max)


def test_movie_with_multiple_producers_credits_each_of_them():
    movies = [
        Movie(
            title="Movie 1",
            year=2000,
            studios=["Studio"],
            producers=["Producer A", "Producer B"],
            winner=True,
        ),
        Movie(
            title="Movie 2",
            year=2003,
            studios=["Studio"],
            producers=["Producer A", "Producer B"],
            winner=True,
        ),
    ]

    result = calculate_producer_intervals(movies)

    assert {interval.producer for interval in result.min} == {
        "Producer A",
        "Producer B",
    }
    assert {interval.producer for interval in result.max} == {
        "Producer A",
        "Producer B",
    }
    assert all(interval.interval == 3 for interval in result.min)


def test_producer_with_single_win_has_no_interval():
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
            producers=["Producer B"],
            winner=True,
        ),
        Movie(
            title="Movie 3",
            year=2010,
            studios=["Studio"],
            producers=["Producer B"],
            winner=True,
        ),
    ]

    result = calculate_producer_intervals(movies)

    all_producers = {interval.producer for interval in result.min} | {
        interval.producer for interval in result.max
    }
    assert "Producer A" not in all_producers


def test_non_winner_movies_are_ignored():
    movies = [
        Movie(
            title="Nominated only",
            year=1999,
            studios=["Studio"],
            producers=["Producer A"],
            winner=False,
        ),
        Movie(
            title="Movie 1",
            year=2000,
            studios=["Studio"],
            producers=["Producer B"],
            winner=True,
        ),
        Movie(
            title="Movie 2",
            year=2004,
            studios=["Studio"],
            producers=["Producer B"],
            winner=True,
        ),
    ]

    result = calculate_producer_intervals(movies)

    all_producers = {interval.producer for interval in result.min} | {
        interval.producer for interval in result.max
    }
    assert all_producers == {"Producer B"}


def test_no_winners_returns_empty_response():
    movies = [
        Movie(
            title="Nominated only",
            year=1999,
            studios=["Studio"],
            producers=["Producer A"],
            winner=False,
        ),
    ]

    result = calculate_producer_intervals(movies)

    assert result.min == []
    assert result.max == []
