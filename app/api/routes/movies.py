from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.movie import Movie
from app.schemas.movie import MovieBase, MovieResponse, MovieUpdate


router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get("/", response_model=list[MovieResponse])
def list_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieBase, db: Session = Depends(get_db)):
    db_movie = Movie(
        title=movie.title,
        year=movie.year,
        studios=movie.studios,
        producers=movie.producers,
        winner=movie.winner,
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie: MovieBase, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db_movie.title = movie.title
    db_movie.year = movie.year
    db_movie.studios = movie.studios
    db_movie.producers = movie.producers
    db_movie.winner = movie.winner
    
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.patch("/{movie_id}", response_model=MovieResponse)
def patch_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie.title is not None:
        db_movie.title = movie.title
    if movie.year is not None:
        db_movie.year = movie.year
    if movie.studios is not None:
        db_movie.studios = movie.studios
    if movie.producers is not None:
        db_movie.producers = movie.producers
    if movie.winner is not None:
        db_movie.winner = movie.winner
    
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.delete("/{movie_id}", response_model=MovieResponse)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete(db_movie)
    db.commit()
    return db_movie