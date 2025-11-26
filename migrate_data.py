import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def migrate_sqlite_to_postgres():
    print("Начинаем перенос данных из SQLite в PostgreSQL...")
    
    # Подключаемся к SQLite
    sqlite_conn = sqlite3.connect('db.sqlite3')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Подключаемся к PostgreSQL
    postgres_conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'film_db'),
        user=os.getenv('POSTGRES_USER', 'film_user'),
        password=os.getenv('POSTGRES_PASSWORD', 'film_password'),
        host=os.getenv('POSTGRES_HOST', 'db'),
        port=os.getenv('POSTGRES_PORT', '5432')
    )
    postgres_cursor = postgres_conn.cursor()
    
    try:
        # Получаем данные из SQLite
        sqlite_cursor.execute("SELECT * FROM movies_film")
        films = sqlite_cursor.fetchall()
        
        print(f"Найдено {len(films)} фильмов в SQLite базе")
        
        # Очищаем существующие данные в PostgreSQL
        postgres_cursor.execute("DELETE FROM movies_film")
        
        # Вставляем данные в PostgreSQL
        for film in films:
            postgres_cursor.execute("""
                INSERT INTO movies_film 
                (id, title, director, year, genre, rating, description, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, film)
        
        postgres_conn.commit()
        print(f"Успешно перенесено {len(films)} фильмов в PostgreSQL")
        
    except Exception as e:
        print(f"Ошибка при переносе: {e}")
        postgres_conn.rollback()
    finally:
        sqlite_conn.close()
        postgres_conn.close()

if __name__ == "__main__":
    migrate_sqlite_to_postgres()