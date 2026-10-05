from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from unidecode import unidecode


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
    )
    title = models.CharField(max_length=200)
    # Добавлено поле slug
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    text = models.TextField()
    image = models.ImageField(upload_to='posts_images/', null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    # Автоматическая генерация слага из заголовка
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)
