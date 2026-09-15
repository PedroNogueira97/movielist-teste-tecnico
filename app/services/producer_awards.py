from collections import defaultdict

from app.models.movie import Movie
from app.schemas.movie import ProducerInterval, ProducerIntervalResponse


def calculate_producer_intervals(
    movies: list[Movie],
) -> ProducerIntervalResponse:
    producer_wins: dict[str, list[int]] = defaultdict(list)

    for movie in movies:
        if not movie.winner:
            continue

        for producer in movie.producers:
            producer_wins[producer].append(movie.year)

    intervals: list[ProducerInterval] = []

    for producer, years in producer_wins.items():
        years.sort()

        for previous_win, following_win in zip(years, years[1:]):
            intervals.append(
                ProducerInterval(
                    producer=producer,
                    interval=following_win - previous_win,
                    previousWin=previous_win,
                    followingWin=following_win,
                )
            )

    if not intervals:
        return ProducerIntervalResponse(min=[], max=[])

    min_interval = min(
        interval.interval
        for interval in intervals
    )

    max_interval = max(
        interval.interval
        for interval in intervals
    )

    return ProducerIntervalResponse(
        min=[
            interval
            for interval in intervals
            if interval.interval == min_interval
        ],
        max=[
            interval
            for interval in intervals
            if interval.interval == max_interval
        ],
    )