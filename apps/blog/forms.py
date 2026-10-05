from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Убедитесь, что 'category' добавлена из предыдущей фазы
        fields = ['title', 'text', 'category', 'image', 'status']
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'category': 'Категория',
            'image': 'Изображение',
            'status': 'Статус',
        }
        # ДОБАВЛЕНО: Тексты-подсказки (help_texts)
        help_texts = {
            'title': 'Придумайте цепляющий заголовок',
            'image': 'Загрузите обложку поста (необязательно)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
