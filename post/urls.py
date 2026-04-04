from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('posts/', views.PostsView.as_view(), name='posts'),
    path('posts/new/', views.CreatePostView.as_view(), name='create_post'),
    path('author/<str:username>/', views.UserPostsView.as_view(), name='user_posts'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/edit/', views.EditPostView.as_view(), name='edit_post'),
    path('posts/<slug:slug>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('posts/<slug:slug>/comment/', views.CreateCommentView.as_view(), name='create_comment'),
    path('posts/<slug:slug>/comment/<int:comment_id>/delete/', views.DeleteCommentView.as_view(),
         name='delete_comment'),
]
