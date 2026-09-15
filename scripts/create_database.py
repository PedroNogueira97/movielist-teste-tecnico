from app.database import Base, engine
from app.models.movie import Movie


Base.metadata.create_all(bind=engine)

print("Database created successfully.")