import pytest
from rest_framework.reverse import reverse
from rest_framework import status

from movies.models import Movie

pytestmark = pytest.mark.django_db

CONTENT_TYPE = "application/json"


class TestListMovies:
    URL = "/api/movies/"
    URL_NAME = "movielens-movies-list"

    def test_url_is_registered(self):
        url = reverse(self.URL_NAME)
        assert self.URL == url

    @pytest.mark.usefixtures("movie")
    def test_should_return_list_of_movies(self, client, movie_data):
        response = client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"] == [movie_data]


class TestCreateMovie:
    URL = "/api/movies/"
    URL_NAME = "movielens-movies-list"

    def test_url_is_registered(self):
        url = reverse(self.URL_NAME)
        assert self.URL == url

    def test_should_create_a_movie_when_valid_data_is_submitted(self, client, genre):
        movie_data = {
            "title": "My Movie 1",
            "genres": [genre.name],
        }
        response = client.post(self.URL, movie_data, content_type=CONTENT_TYPE)
        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.data.copy()
        movie_id = response_data.pop("id")
        assert response_data == movie_data
        actual_movie = Movie.objects.get(id=movie_id)
        assert "My Movie 1" == actual_movie.title
        assert [genre] == list(actual_movie.genres.all())

    def test_should_not_allow_to_create_movie_when_genre_does_not_exist(self, client):
        genre_name = "Non-Existing-Genre-Name"
        movie_data = {
            "title": "My Movie 1",
            "genres": [genre_name],
        }
        response = client.post(self.URL, movie_data, content_type=CONTENT_TYPE)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        expect_msg = f"Object with name={genre_name} does not exist"
        assert expect_msg in response.content.decode()

    def test_should_allow_creating_movie_without_genres(self, client):
        movie_data = {
            "title": "My Movie 1",
            "genres": [],
        }
        response = client.post(self.URL, movie_data, content_type=CONTENT_TYPE)
        assert response.status_code == status.HTTP_201_CREATED


class TestRetrieveMovie:
    URL = "/api/movies/{movie.id}/"

    def test_should_return_movie_when_movie_exists(self, client, movie):
        url = self.URL.format(movie=movie)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert movie.id == response.data["id"]
        assert movie.title == response.data["title"]

    def test_should_return_404_when_movie_id_does_not_exist(self, client, movie):
        url = self.URL.format(movie=movie)
        movie.delete()
        response = client.get(url, content_type=CONTENT_TYPE)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateMovie:
    URL = "/api/movies/{movie.id}/"

    def test_should_update_existing_movie(self, client, movie, genre):
        data = {"title": "Updated title", "genres": [genre.name]}
        url = self.URL.format(movie=movie)
        response = client.put(url, data, content_type=CONTENT_TYPE)
        assert response.status_code == status.HTTP_200_OK
        movie.refresh_from_db()
        assert "Updated title" == movie.title
        assert [genre] == list(movie.genres.all())

    def test_should_return_404_when_updating_non_existent_movie(self, client, movie):
        url = self.URL.format(movie=movie)
        movie.delete()
        response = client.put(url, {}, content_type=CONTENT_TYPE)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestPatchMovie:
    URL = "/api/movies/{movie.id}/"

    def test_should_update_only_title(self, client, movie_with_genre, genre):
        data = {"title": "Updated Title"}
        url = self.URL.format(movie=movie_with_genre)
        response = client.patch(url, data, content_type=CONTENT_TYPE)
        assert response.status_code == status.HTTP_200_OK
        movie_with_genre.refresh_from_db()
        assert "Updated Title" == movie_with_genre.title
        assert [genre] == list(movie_with_genre.genres.all())

    def test_should_update_only_genres(self, client, movie, genre):
        original_title = movie.title
        data = {"genres": [genre.name]}
        url = self.URL.format(movie=movie)
        response = client.patch(url, data, content_type=CONTENT_TYPE)
        assert response.status_code == status.HTTP_200_OK
        movie.refresh_from_db()
        assert original_title == movie.title
        assert [genre] == list(movie.genres.all())

    def test_should_return_404_when_patching_non_existent_movie(self, client, movie):
        url = self.URL.format(movie=movie)
        movie.delete()
        response = client.patch(url, {}, content_type=CONTENT_TYPE)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteMovie:
    URL = "/api/movies/{movie.id}/"

    def test_should_delete_existing_movie(self, client, movie):
        url = self.URL.format(movie=movie)
        response = client.delete(url, content_type=CONTENT_TYPE)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(Movie.DoesNotExist):
            movie.refresh_from_db()

    def test_should_return_404_when_deleting_non_existent_movie(self, client, movie):
        url = self.URL.format(movie=movie)
        movie.delete()
        response = client.delete(url, content_type=CONTENT_TYPE)
        assert response.status_code == status.HTTP_404_NOT_FOUND
