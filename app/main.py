"""FastAPI application entrypoint.

Golden Raspberry Awards API - skeleton only, no routes registered yet.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Golden Raspberry Awards API",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
