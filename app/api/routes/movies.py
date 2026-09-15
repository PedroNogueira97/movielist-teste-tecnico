"""Routes for the /movies resource.

Not implemented yet: this router is not registered on the app yet.
"""

@router.get("/movies", response_model=list[MovieResponse])
async def get_movies():
    ...