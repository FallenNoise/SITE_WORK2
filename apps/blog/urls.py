from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('post/add/', views.post_add, name='post_add'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
]
