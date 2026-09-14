from django import forms


class PostForm(forms.Form):
    title = forms.CharField(max_length=200, label="Заголовок")
    text = forms.CharField(widget=forms.Textarea, label="Текст")
