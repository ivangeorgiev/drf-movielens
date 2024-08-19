# movies/management/commands/import_movies.py
import csv
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, MovieGenre


IGNORE_GENRES = ["(no genres listed)"]

class Command(BaseCommand):
    help = "Import movies from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="The path to the CSV file to be imported"
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        Movie.objects.all().delete()
        Genre.objects.all().delete()

        movies = []
        genre_names_by_movie = {}
        genre_names = set()

        try:
            with open(csv_file, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    movie = Movie(id=row["movieId"], title=row["title"].strip())
                    movies.append(movie)
                    this_movie_genres = [g.strip() for g in row["genres"].split("|")]
                    genre_names_by_movie[movie.id] = this_movie_genres
                    genre_names.update(g for g in this_movie_genres if g not in IGNORE_GENRES)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    "File not found. Please provide a valid CSV file path."
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

        Movie.objects.bulk_create(movies)

        genres_by_name = {
            name: Genre(id=i + 1, name=name) for i, name in enumerate(genre_names)
        }
        Genre.objects.bulk_create(genres_by_name.values())

        all_movie_genres = []
        for movie_id, this_movie_genres in genre_names_by_movie.items():
            for genre_name in this_movie_genres:
                if genre_name not in genres_by_name:
                    continue
                genre = genres_by_name[genre_name]
                movie_genre = MovieGenre(movie_id=movie_id, genre=genre)
                all_movie_genres.append(movie_genre)
        MovieGenre.objects.bulk_create(all_movie_genres)
