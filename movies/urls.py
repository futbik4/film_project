from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_film, name='add_film'),
    path('export/', views.export_films, name='export_films'),
    path('import/', views.import_films, name='import_films'),
    path('list/', views.film_list, name='film_list'),
    path('api/films/search/', views.film_search, name='film_search'),
    path('film/edit/<int:film_id>/', views.edit_film, name='edit_film'),
    path('film/delete/<int:film_id>/', views.delete_film, name='delete_film'),
]
