from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # ДОБАВЛЕНО: 'tags' в fields
        fields = ['title', 'text', 'category', 'tags', 'image', 'status'] 
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'category': 'Категория',
            'tags': 'Теги', # ДОБАВЛЕНО
            'image': 'Изображение',
            'status': 'Статус',
        }
        help_texts = {
            'title': 'Придумайте цепляющий заголовок',
            'image': 'Загрузите обложку поста (необязательно)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            # ДОБАВЛЕНО: SelectMultiple позволяет зажать Ctrl (Windows) и выбрать несколько тегов сразу
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}), 
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }