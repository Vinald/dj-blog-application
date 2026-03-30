from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='post-index'),
    path('about/', views.about, name='post-about'),
    path('posts/', views.posts, name='posts'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
]