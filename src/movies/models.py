from django.db import models


class Genre(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "ml_genre"

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre, through="MovieGenre")

    class Meta:
        db_table = "ml_movie"

    def __str__(self) -> str:
        return self.title


class MovieGenre(models.Model):
    id = models.BigAutoField(primary_key=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        db_table = "ml_movie_genre"
