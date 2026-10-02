from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Добавляем поле author. CASCADE означает, что при удалении пользователя удалятся и его посты.
    # null=True временно нужен, чтобы не сломать существующие в БД посты без авторов.
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
