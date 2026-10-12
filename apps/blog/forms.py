from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    # Добавлено текстовое поле для ручного ввода тегов
    tags_input = forms.CharField(
        required=False,
        label='Теги',
        help_text='Введите теги через запятую (например: django, python, web)',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'тег1, тег2...'})
    )

    class Meta:
        model = Post
        # Поле 'tags' убрано, так как обрабатывается вручную
        fields = ['title', 'text', 'category', 'image', 'status']
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'category': 'Категория',
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
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если пост редактируется, подтягиваем его существующие теги в строку
        if self.instance and self.instance.pk:
            self.fields['tags_input'].initial = ', '.join(
                [tag.name for tag in self.instance.tags.all()])
