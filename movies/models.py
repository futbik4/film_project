from django.db import models

class Film(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название фильма")
    director = models.CharField(max_length=100, verbose_name="Режиссер")
    year = models.IntegerField(verbose_name="Год выпуска")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    rating = models.FloatField(verbose_name="Рейтинг")
    description = models.TextField(verbose_name="Описание", blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"