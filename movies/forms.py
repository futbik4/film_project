from django import forms
from .models import Film

class FilmForm(forms.ModelForm):
    SAVE_CHOICES = [
        ('db', 'Сохранить в базу данных'),
        ('json', 'Сохранить в JSON файл'),
    ]
    
    save_location = forms.ChoiceField(
        choices=SAVE_CHOICES,
        initial='db',
        widget=forms.RadioSelect,
        label='Куда сохранить данные?'
    )
    
    class Meta:
        model = Film
        fields = ['title', 'director', 'year', 'genre', 'rating', 'description', 'country']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_year(self):
        year = self.cleaned_data['year']
        if year < 1888:
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