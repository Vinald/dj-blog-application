from django.shortcuts import render


def index(request):
    return render(request, "blog/index.html")


def posts(request):
    return render(request, "blog/posts.html")


def post_detail(request, slug):
    return render(request, "blog/post_detail.html", {"slug": slug})