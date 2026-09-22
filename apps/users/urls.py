from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
]
