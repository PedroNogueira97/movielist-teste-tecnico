from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import database
from app.api.routes import movies
from scripts.import_csv import import_movies


def create_tables_and_import_movies() -> None:
    """Create tables (if needed) and import the CSV dataset (idempotent).

    Reads `database.engine`/`database.SessionLocal` at call time (rather
    than importing them by name) so tests can point the app at an
    isolated database before triggering this via the lifespan below.
    """
    database.Base.metadata.create_all(bind=database.engine)
    import_movies()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables_and_import_movies()
    yield


app = FastAPI(
    title="Golden Raspberry Awards API",
    description=(
        "API REST para consulta dos indicados e vencedores "
        "da categoria Pior Filme do Golden Raspberry Awards."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(movies.router)
