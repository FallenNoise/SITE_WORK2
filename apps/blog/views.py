from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.text import slugify
from unidecode import unidecode
from .models import Post, Category, Tag
from .forms import PostForm


def home_page(request):
    posts = Post.objects.all()[:3]
    return render(request, 'pages/index.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'pages/post_list.html', {'posts': posts})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    return render(request, 'pages/post_list.html', {'posts': posts, 'category': category})


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    return render(request, 'pages/post_list.html', {'posts': posts, 'tag': tag})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'pages/post_detail.html', {'post': post})


@login_required
def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Ручная обработка тегов
            tags_str = form.cleaned_data.get('tags_input', '')
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            for tag_name in tag_names:
                tag_slug = slugify(unidecode(tag_name))
                tag, _ = Tag.objects.get_or_create(
                    slug=tag_slug, defaults={'name': tag_name})
                post.tags.add(tag)

            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'pages/post_form.html', {'form': form})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать чужой пост.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()

            # Очищаем старые теги и сохраняем новые
            post.tags.clear()
            tags_str = form.cleaned_data.get('tags_input', '')
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            for tag_name in tag_names:
                tag_slug = slugify(unidecode(tag_name))
                tag, _ = Tag.objects.get_or_create(
                    slug=tag_slug, defaults={'name': tag_name})
                post.tags.add(tag)

            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'pages/post_form.html', {'form': form})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить чужой пост.")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'pages/post_confirm_delete.html', {'post': post})
