import pytest
from movies.models import Genre, Movie


@pytest.mark.django_db
class TestMovie:
    def test_can_create_movie(self):
        movie = Movie.objects.create(title="Movie 1")
        assert isinstance(movie, Movie)

    def test_can_get_movie_by_id(self, movie: Movie):
        actual_movie = Movie.objects.get(id=movie.id)
        assert movie.title == actual_movie.title

    def test_can_delete_movie(self, movie: Movie):
        movie.delete()
        with pytest.raises(Movie.DoesNotExist):
            Movie.objects.get(id=movie.id)

    def test_can_assign_genre(self, movie: Movie, genre: Genre):
        movie.genres.set([genre])
        movie.refresh_from_db()
        assert [genre] == list(movie.genres.all())

    def test_can_access_movies_from_genre(self, movie_with_genre: Movie, genre: Genre):
        assert [movie_with_genre] == list(genre.movies.all())

@pytest.mark.django_db
class TestGenre:
    def test_can_get_genre_by_id(self, genre: Genre):
        actual_genre = Genre.objects.get(id=genre.id)
        assert genre.name == actual_genre.name
