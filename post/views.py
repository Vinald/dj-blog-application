from django.shortcuts import render


def index(request):
    context = {
        'posts': []  # Empty list for now, populate when models are created
    }
    return render(request, "post/index.html", context)


def about(request):
    return render(request, "post/about.html")


def posts(request):
    return render(request, "post/posts.html")


def post_detail(request, slug):
    return render(request, "post/post_detail.html", {"slug": slug})