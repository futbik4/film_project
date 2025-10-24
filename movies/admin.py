from django.contrib import admin
from .models import Film

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'year', 'genre', 'rating']
    list_filter = ['year', 'genre', 'rating']
    search_fields = ['title', 'director', 'description']
    ordering = ['-rating']
