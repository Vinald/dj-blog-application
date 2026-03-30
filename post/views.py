from django.shortcuts import render
from django.template.defaultfilters import title


def index(request):
    context = {
        'posts': []  # Empty list for now, populate when models are created
    }
    return render(request, "post/index.html", {"context": context, "title": "Home"})


def about(request):
    return render(request, "post/about.html")


def posts(request):
    return render(request, "post/posts.html", {"title": "Posts"})  # Empty list for now


def post_detail(request, slug):
    return render(request, "post/post_detail.html", {"slug": slug, "title": title(slug.replace('-', ' '))})