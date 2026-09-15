from sqlalchemy import Boolean, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Movie(Base):
    """Movie database model."""
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True
    )

    title: Mapped[str] = mapped_column(
        String, 
        nullable=False
    )

    year: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )

    studios: Mapped[list[str]] = mapped_column(
        JSON, 
        nullable=False
    )

    producers: Mapped[list[str]] = mapped_column(
        JSON, 
        nullable=False
    )
    
    winner: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False,
        default=False,
    )