from django.shortcuts import render, get_object_or_404
from .models import Post
from django.shortcuts import redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def home_page(request):
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'pages/index.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'pages/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'pages/post_detail.html', {'post': post})


@login_required
def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Сохраняем форму, но пока не отправляем в БД (commit=False)
            post = form.save(commit=False)
            # Присваиваем текущего пользователя в качестве автора
            post.author = request.user
            # Теперь сохраняем в БД
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'pages/post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Проверка: является ли текущий пользователь автором поста?
    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать чужой пост.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'pages/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Проверка: является ли текущий пользователь автором поста?
    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить чужой пост.")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'pages/post_confirm_delete.html', {'post': post})
