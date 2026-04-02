from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('posts/', views.posts, name='posts'),
    path('posts/new/', views.create_post, name='create_post'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('posts/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('posts/<slug:slug>/delete/', views.delete_post, name='delete_post'),
]
