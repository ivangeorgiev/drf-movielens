# movies/serializers.py
from rest_framework import serializers
from movies.models import Movie, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(many=True, queryset=Genre.objects.all(), slug_field="name")

    class Meta:
        model = Movie
        fields = "__all__"
