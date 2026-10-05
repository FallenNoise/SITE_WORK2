from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse  # ДОБАВЛЕНО: функция reverse
from unidecode import unidecode


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    # ДОБАВЛЕНО: получение ссылки на категорию
    def get_absolute_url(self):
        return reverse('category_posts', kwargs={'slug': self.slug})


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    text = models.TextField()
    image = models.ImageField(upload_to='posts_images/', null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='posts', verbose_name="Категория")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    # ДОБАВЛЕНО: получение ссылки на сам пост
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)
