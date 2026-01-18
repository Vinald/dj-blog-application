from django.shortcuts import render
from .models import Post


def home(request):
    context = {"posts": Post.objects.all(), "title": "Home"}
    return render(request, "blog/home.html", context)


def about(request):
    context = {"title": "About"}
    return render(request, "blog/about.html", context)
