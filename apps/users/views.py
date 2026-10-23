from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.blog.models import Post


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    next_page = 'home'


class CustomLogoutView(LogoutView):
    next_page = 'home'


class ProfileView(ListView):
    model = Post
    template_name = 'users/profile.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        self.profile_user = get_object_or_404(
            User, username=self.kwargs['username'])
        return Post.objects.filter(author=self.profile_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.profile_user
        return context
