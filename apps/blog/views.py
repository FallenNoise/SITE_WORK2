from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.text import slugify
from unidecode import unidecode
from .models import Post, Category, Tag
from .forms import PostForm


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

    # ДОБАВЛЕНО: Логика увеличения просмотров и сохранения пользователей
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # Увеличиваем счетчик общих просмотров (update_fields ускоряет запрос)
        obj.views += 1
        obj.save(update_fields=['views'])

        # Добавляем пользователя в список посмотревших, если он авторизован
        if self.request.user.is_authenticated:
            obj.viewed_by_users.add(self.request.user)

        return obj


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
