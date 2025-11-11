import json
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .forms import FilmForm
from .models import Film
from django.contrib import messages
from django.db import models

def home(request):
    return render(request, 'home.html')

def add_film(request):
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            save_location = form.cleaned_data['save_location']
            film_data = form.cleaned_data
            
            if save_location == 'db':
                duplicate = Film.objects.filter(
                    title=film_data['title'],
                    director=film_data['director'], 
                    year=film_data['year']
                ).exists()
                
                if duplicate:
                    messages.warning(request, f'Фильм "{film_data["title"]}" уже есть в базе!')
                    return render(request, 'add_film.html', {'form': form})
                
                film = form.save()
                messages.success(request, f'Фильм "{film.title}" сохранен в БД!')
                
            elif save_location == 'json':
                data_dir = os.path.join(settings.MEDIA_ROOT, 'film_data')
                os.makedirs(data_dir, exist_ok=True)
                json_file_path = os.path.join(data_dir, 'films.json')
                
                films_list = []
                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r', encoding='utf-8') as f:
                        films_list = json.load(f)
                
                films_list.append({
                    'title': film_data['title'],
                    'director': film_data['director'],
                    'year': film_data['year'],
                    'genre': film_data['genre'], 
                    'rating': film_data['rating'],
                    'description': film_data['description'],
                    'country': film_data['country']
                })
                
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    json.dump(films_list, f, ensure_ascii=False, indent=2)
                
                messages.success(request, f'Фильм "{film_data["title"]}" сохранен в JSON!')
            
            return redirect('add_film')
    else:
        form = FilmForm()
    
    return render(request, 'add_film.html', {'form': form})

def export_films(request):
    films = Film.objects.all()
    films_count = films.count()
    
    if request.method == 'POST':
        format_type = request.POST.get('format')
        
        if not films:
            messages.warning(request, 'Нет фильмов для экспорта')
            return redirect('export_films')
        
        if format_type == 'json':
            films_data = []
            for film in films:
                films_data.append({
                    'title': film.title,
                    'director': film.director,
                    'year': film.year,
                    'genre': film.genre,
                    'rating': film.rating,
                    'description': film.description,
                    'country': film.country
                })
            
            response = HttpResponse(json.dumps(films_data, ensure_ascii=False, indent=2), 
                                  content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="films.json"'
            return response
    
    return render(request, 'export_films.html', {'films_count': films_count})

def import_films(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        import_dir = os.path.join(settings.MEDIA_ROOT, 'imports')
        os.makedirs(import_dir, exist_ok=True)
        
        file_path = os.path.join(import_dir, uploaded_file.name)
        
        try:
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            if file_extension == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    films_data = json.load(f)
                
                for film_data in films_data:
                    Film.objects.get_or_create(
                        title=film_data['title'],
                        defaults={
                            'director': film_data.get('director', ''),
                            'year': film_data.get('year', 0),
                            'genre': film_data.get('genre', ''),
                            'rating': film_data.get('rating', 0),
                            'description': film_data.get('description', ''),
                            'country': film_data.get('country', '')

                        }
                    )           
            else:
                messages.error(request, 'Неподдерживаемый формат файла')
                os.remove(file_path)
                return redirect('import_films')
            
            os.remove(file_path)
            messages.success(request, 'Фильмы успешно импортированы!')
            
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            messages.error(request, f'Ошибка при импорте файла: {str(e)}')
    
    return render(request, 'import_films.html')

def film_list(request):
    source = request.GET.get('source', 'db')
    
    if source == 'file':
        films = []
        try:
            json_file_path = os.path.join(settings.MEDIA_ROOT, 'film_data', 'films.json')
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    films_data = json.load(f)
                
                for film_data in films_data:
                    films.append(type('Film', (), {
                        'title': film_data.get('title', ''),
                        'director': film_data.get('director', ''),
                        'year': film_data.get('year', 0),
                        'genre': film_data.get('genre', ''),
                        'rating': film_data.get('rating', 0),
                        'description': film_data.get('description', ''),
                        'country': film_data.get('country', '')
                    })())
        except Exception as e:
            messages.error(request, f'Ошибка при загрузке из файлов: {str(e)}')
    else:
        films = Film.objects.all()
    
    return render(request, 'film_list.html', {'films': films})

from django.http import JsonResponse

def film_search(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '')
        films = Film.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(director__icontains=query) |
            models.Q(genre__icontains=query) |
            models.Q(country__icontains=query)
        )
        films_data = []
        for film in films:
            films_data.append({
                'id': film.id,
                'title': film.title,
                'director': film.director,
                'year': film.year,
                'genre': film.genre,
                'rating': film.rating,
                'description': film.description,
                'country': film.country
            })
        return JsonResponse(films_data, safe=False)
    return JsonResponse([], safe=False)

def edit_film(request, film_id):
    film = Film.objects.get(id=film_id)
    if request.method == 'POST':
        form = FilmForm(request.POST, instance=film)
        if form.is_valid():
            form.save()
            messages.success(request, f'Фильм "{film.title}" успешно обновлен!')
            return redirect('film_list')
    else:
        form = FilmForm(instance=film)
    return render(request, 'edit_film.html', {'form': form, 'film': film})

def delete_film(request, film_id):
    film = Film.objects.get(id=film_id)
    if request.method == 'POST':
        title = film.title
        film.delete()
        messages.success(request, f'Фильм "{title}" успешно удален!')
        return redirect('film_list')
    return render(request, 'delete_film.html', {'film': film})