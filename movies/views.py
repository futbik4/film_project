import json
import xml.etree.ElementTree as ET
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .forms import FilmForm
from .models import Film
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def add_film(request):
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            film = form.save()
            messages.success(request, f'Фильм "{film.title}" успешно добавлен!')
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
                    'description': film.description
                })
            
            response = HttpResponse(json.dumps(films_data, ensure_ascii=False, indent=2), 
                                  content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="films.json"'
            return response
            
        elif format_type == 'xml':
            root = ET.Element('films')
            for film in films:
                film_elem = ET.SubElement(root, 'film')
                ET.SubElement(film_elem, 'title').text = film.title
                ET.SubElement(film_elem, 'director').text = film.director
                ET.SubElement(film_elem, 'year').text = str(film.year)
                ET.SubElement(film_elem, 'genre').text = film.genre
                ET.SubElement(film_elem, 'rating').text = str(film.rating)
                ET.SubElement(film_elem, 'description').text = film.description
            
            response = HttpResponse(ET.tostring(root, encoding='utf-8'), 
                                  content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename="films.xml"'
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
                            'description': film_data.get('description', '')
                        }
                    )
                
            elif file_extension == '.xml':
                tree = ET.parse(file_path)
                root = tree.getroot()
                
                for film_elem in root.findall('film'):
                    Film.objects.get_or_create(
                        title=film_elem.find('title').text,
                        defaults={
                            'director': film_elem.find('director').text if film_elem.find('director') is not None else '',
                            'year': int(film_elem.find('year').text) if film_elem.find('year') is not None else 0,
                            'genre': film_elem.find('genre').text if film_elem.find('genre') is not None else '',
                            'rating': float(film_elem.find('rating').text) if film_elem.find('rating') is not None else 0,
                            'description': film_elem.find('description').text if film_elem.find('description') is not None else ''
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
    films = Film.objects.all()
    return render(request, 'film_list.html', {'films': films})
