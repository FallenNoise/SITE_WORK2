from django.shortcuts import render, get_object_or_404
from .models import Post
from django.shortcuts import redirect
from .forms import PostForm


def home_page(request):
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'pages/index.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'pages/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'pages/post_detail.html', {'post': post})


def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text']
            )
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'pages/post_add.html', {'form': form})
