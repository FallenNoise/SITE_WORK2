from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/add/', views.PostCreateView.as_view(), name='post_add'),
    path('category/<slug:slug>/',
         views.CategoryPostListView.as_view(), name='category_posts'),
    path('tag/<slug:slug>/', views.TagPostListView.as_view(), name='tag_posts'),
    # ДОБАВЛЕНО: Маршрут поиска
    path('search/', views.PostSearchView.as_view(), name='post_search'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/',
         views.PostDeleteView.as_view(), name='post_delete'),
]
