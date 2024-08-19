# movies/views.py
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from movies.models import Movie, Genre
from .serializers import MovieSerializer, GenreSerializer

class CustomPageNumberPagination(PageNumberPagination):
    pass

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CustomPageNumberPagination


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = CustomPageNumberPagination
