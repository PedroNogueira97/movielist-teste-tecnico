import csv
from pathlib import Path

from app.database import SessionLocal
from app.models.movie import Movie
from app.schemas.movie import MovieBase


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "Movielist.csv"

def normalize_winner(value: str) -> bool:
    value = value.strip().lower()

    if value == "yes":
        return True

    if value == "":
        return False

    raise ValueError(f"Valor inválido para winner: {value!r}")


def normalize_row(row: dict[str, str]) -> MovieBase:
    studios = [
        studio.strip()
        for studio in row["studios"].split(",")
        if studio.strip()
    ]

    winner = normalize_winner(row["winner"])

    return MovieBase(
        title=row["title"].strip(),
        year=int(row["year"]),
        studios=studios,
        producers=row["producers"].strip(),
        winner=winner,
    )


def import_movies() -> None:
    db = SessionLocal()

    try:
        with CSV_PATH.open(
            mode="r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file, delimiter=";")

            movies = []

            for row in reader:
                movie_data = normalize_row(row)

                movie = Movie(
                    title=movie_data.title,
                    year=movie_data.year,
                    studios=movie_data.studios,
                    producers=movie_data.producers,
                    winner=movie_data.winner,
                )

                movies.append(movie)

            db.add_all(movies)
            db.commit()

            print(f"{len(movies)} filmes importados com sucesso.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import_movies()