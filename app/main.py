from fastapi import FastAPI

from app.api.routes import movies


app = FastAPI(
    title="Golden Raspberry Awards API",
    description=(
        "API REST para consulta dos indicados e vencedores "
        "da categoria Pior Filme do Golden Raspberry Awards."
    ),
    version="1.0.0",
)

app.include_router(movies.router)