from django import forms
from .models import Film

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['title', 'director', 'year', 'genre', 'rating', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_year(self):
        year = self.cleaned_data['year']
        if year < 1888:  # Первый фильм был снят в 1888
            raise forms.ValidationError('Год не может быть меньше 1888')
        if year > 2030:
            raise forms.ValidationError('Год не может быть больше 2030')
        return year
    
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0:
            raise forms.ValidationError('Рейтинг не может быть отрицательным')
        if rating > 10:
            raise forms.ValidationError('Рейтинг не может быть больше 10')
        return rating
