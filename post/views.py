from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import Post
from .forms import PostForm


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


@require_http_methods(["GET", "POST"])
@login_required(login_url='account:login')
def create_post(request):
    """Create a new blog post."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', slug=post.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PostForm()

    return render(request, 'post/create_post.html', {'form': form})


@require_http_methods(["GET", "POST"])
@login_required(login_url='account:login')
def edit_post(request, slug):
    """Edit an existing blog post."""
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('post_detail', slug=post.slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', slug=post.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PostForm(instance=post)

    return render(request, 'post/edit_post.html', {'form': form, 'post': post})


@require_http_methods(["GET", "POST"])
@login_required(login_url='account:login')
def delete_post(request, slug):
    """Delete a blog post."""
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('post_detail', slug=post.slug)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('index')

    return render(request, 'post/delete_post.html', {'post': post})

