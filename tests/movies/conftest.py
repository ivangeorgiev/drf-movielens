import pytest
from movies.models import Genre, Movie


@pytest.fixture(name="movie")
def given_movie() -> Movie:
    movie = Movie.objects.create(id=1, title="Movie 1")
    return movie


@pytest.fixture(name="genre")
def given_genre() -> Genre:
    genre = Genre.objects.create(id=1, name="Genre 1")
    return genre


@pytest.fixture(name="movie_with_genre")
def given_movie_with_genre(movie, genre):
    movie.genres.set([genre])
    return movie
