from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
    )
    title = models.CharField(max_length=200)
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
