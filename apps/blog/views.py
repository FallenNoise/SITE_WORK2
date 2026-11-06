from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from unidecode import unidecode

from .forms import PostForm, CommentForm
from .models import Category, Post, Tag, Comment


class HomeView(ListView):
    model = Post
    template_name = 'pages/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()[:3]


class PostListView(ListView):
    model = Post
    template_name = 'pages/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5


class CategoryPostListView(ListView):
    model = Post
    template_name = 'pages/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.category, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostListView(ListView):
    model = Post
    template_name = 'pages/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(tags=self.tag, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'pages/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save(update_fields=['views'])
        if self.request.user.is_authenticated:
            obj.viewed_by_users.add(self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'pages/post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        tags_str = form.cleaned_data.get('tags_input', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        for tag_name in tag_names:
            tag_slug = slugify(unidecode(tag_name))
            tag, _ = Tag.objects.get_or_create(
                slug=tag_slug, defaults={'name': tag_name})
            self.object.tags.add(tag)
        messages.success(self.request, "Пост успешно создан!")
        return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'pages/post_form.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.tags.clear()
        tags_str = form.cleaned_data.get('tags_input', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        for tag_name in tag_names:
            tag_slug = slugify(unidecode(tag_name))
            tag, _ = Tag.objects.get_or_create(
                slug=tag_slug, defaults={'name': tag_name})
            self.object.tags.add(tag)
        return response


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'pages/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        return self.request.user == self.get_object().author


class PostSearchView(ListView):
    model = Post
    template_name = 'pages/posts_search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(text__icontains=query) |
                Q(category__name__icontains=query) |
                Q(tags__name__icontains=query),
                status='published'
            ).distinct()
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if request.user in post.disliked_by_users.all():
            post.disliked_by_users.remove(request.user)
        if request.user in post.liked_by_users.all():
            post.liked_by_users.remove(request.user)
        else:
            post.liked_by_users.add(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class PostDislikeView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if request.user in post.liked_by_users.all():
            post.liked_by_users.remove(request.user)
        if request.user in post.disliked_by_users.all():
            post.disliked_by_users.remove(request.user)
        else:
            post.disliked_by_users.add(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class PostFavoriteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if request.user in post.favorites.all():
            post.favorites.remove(request.user)
            messages.info(request, "Пост удален из избранного.")
        else:
            post.favorites.add(request.user)
            messages.success(request, "Пост добавлен в избранное!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class FavoritePostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'pages/favorite_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return self.request.user.favorite_posts.filter(status='published')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, slug=self.kwargs['slug'])
        messages.success(self.request, "Комментарий успешно добавлен!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.kwargs['slug']})
