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

class MovieResponde(MovieBase):
    """Schema for movie response data."""
    id: int