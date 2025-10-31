# Django Film Management App

Приложение для управления информацией о фильмах с возможностью импорта/экспорта в JSON и XML форматах.

## Функциональность

-  Добавление фильмов через веб-форму
-  Валидация вводимых данных
-  Импорт фильмов из JSON/XML файлов
-  Экспорт фильмов в JSON/XML форматы
-  Просмотр списка всех фильмов
-  Административная панель Django

## Установка и запуск

1. **Клонируйте репозиторий:**
```
git clone <https://github.com/futbik4/film_project>
cd film_project
```
2. **Создайте виртуальное окружение:**
```
py -m venv venv
```
3. **Активируйте виртуальное окружение:**
```
venv\Scripts\activate
```
4. **Установите зависимости:**
```
pip install -r requirements.txt
```
6. **Выполнить миграции**
```
py manage.py makemigrations
py manage.py migrate
```
7. **Запустите сервер:**
```
py manage.py runserver
```
8. **Откройте в браузере:**
<http://127.0.0.1:8000/>

## Технологии
- Django 5.2
- HTML5/CSS3
- SQLite
- JSON/XML парсеры Python