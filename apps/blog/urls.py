from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/add/', views.PostCreateView.as_view(), name='post_add'),
    path('category/<slug:slug>/',
         views.CategoryPostListView.as_view(), name='category_posts'),
    path('tag/<slug:slug>/', views.TagPostListView.as_view(), name='tag_posts'),
    path('search/', views.PostSearchView.as_view(), name='post_search'),
    path('favorites/', views.FavoritePostsListView.as_view(), name='favorite_posts'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/',
         views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('post/<slug:slug>/dislike/',
         views.PostDislikeView.as_view(), name='post_dislike'),
    path('post/<slug:slug>/favorite/',
         views.PostFavoriteView.as_view(), name='post_favorite'),
    path('post/<slug:slug>/comment/',
         views.CommentCreateView.as_view(), name='post_comment'),
]
