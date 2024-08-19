from django.contrib import admin
from .models import Movie, Genre, MovieGenre

class MovieGenreInline(admin.TabularInline):
    model = MovieGenre
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', )
    inlines = [MovieGenreInline]

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

class MovieGenreAdmin(admin.ModelAdmin):
    list_display = ('movie', 'genre')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(MovieGenre, MovieGenreAdmin)
