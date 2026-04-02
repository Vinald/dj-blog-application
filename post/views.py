from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Post
from .forms import PostForm


class IndexView(ListView):
    """Class-based view for displaying all posts on home page."""
    model = Post
    template_name = 'post/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class AboutView(View):
    """Class-based view for about page."""

    def get(self, request):
        return render(request, 'post/about.html')


class PostsView(ListView):
    """Class-based view for displaying all posts listing page."""
    model = Post
    template_name = 'post/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Posts'
        return context


class PostDetailView(DetailView):
    """Class-based view for displaying a single post detail."""
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class CreatePostView(LoginRequiredMixin, View):
    """Class-based view for creating a new blog post."""
    login_url = 'account:login'
    template_name = 'post/create_post.html'

    def get(self, request):
        form = PostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
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

        return render(request, self.template_name, {'form': form})


class EditPostView(LoginRequiredMixin, View):
    """Class-based view for editing an existing blog post."""
    login_url = 'account:login'
    template_name = 'post/edit_post.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if request.user != post.author:
            messages.error(request, 'You can only edit your own posts.')
            return redirect('post_detail', slug=post.slug)

        form = PostForm(instance=post)
        return render(request, self.template_name, {'form': form, 'post': post})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if request.user != post.author:
            messages.error(request, 'You can only edit your own posts.')
            return redirect('post_detail', slug=post.slug)

        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', slug=post.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return render(request, self.template_name, {'form': form, 'post': post})


class DeletePostView(LoginRequiredMixin, View):
    """Class-based view for deleting a blog post."""
    login_url = 'account:login'
    template_name = 'post/delete_post.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if request.user != post.author:
            messages.error(request, 'You can only delete your own posts.')
            return redirect('post_detail', slug=post.slug)

        return render(request, self.template_name, {'post': post})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if request.user != post.author:
            messages.error(request, 'You can only delete your own posts.')
            return redirect('post_detail', slug=post.slug)

        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('index')
