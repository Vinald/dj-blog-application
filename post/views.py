from django.shortcuts import render

from .models import Post


def index(request):
    all_posts = Post.objects.all()

    context = {
        'posts': all_posts,
        "title": "Home"
    }
    return render(request, "post/index.html", context)


def about(request):
    return render(request, "post/about.html")


def posts(request):
    all_posts = Post.objects.all()
    context = {
        'posts': all_posts,
        "title": "Posts"
    }
    return render(request, "post/posts.html", context)


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    context = {
        'post': post,
        'title': post.title
    }
    return render(request, "post/post_detail.html", context)
