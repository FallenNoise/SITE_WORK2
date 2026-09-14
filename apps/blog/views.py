from django.shortcuts import render, get_object_or_404
from .models import Post


def home_page(request):
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'pages/index.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'pages/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'pages/post_detail.html', {'post': post})
