from django.shortcuts import render
from .models import Post


def home_page(request):
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'pages/index.html', {'posts': posts})
