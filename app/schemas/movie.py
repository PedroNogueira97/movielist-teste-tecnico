"""Pydantic schemas for movie input/output.

Not implemented yet.
"""
from pydantic import BaseModel

class MovieBase(BaseModel):
    """Base schema for movie data."""
    title: str
    year: int
    studios: list[str]
    producers: str
    winner: bool

class MovieResponse(MovieBase):
    """Schema for movie response data."""
    id: int

class MovieUpdate(BaseModel):
    title: str | None = None
    year: int | None = None
    studios: list[str] | None = None
    producers: str | None = None
    winner: bool | None = None