from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post, Comment
from .forms import PostForm, CommentForm


class UserOwnsObjectMixin(UserPassesTestMixin):
    """Mixin to check if user owns the object."""

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author

    def handle_no_permission(self):
        """Redirect to the login page if user doesn't own the object."""
        return redirect('account:login')


class UserOwnsCommentMixin(UserPassesTestMixin):
    """Mixin to check if user owns the comment or is the post author."""

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user == comment.post.author


class FormErrorMessagesMixin:
    """Mixin to add form errors as messages."""

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)


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

    def get(self, request, *args, **kwargs):
        # Track page visits in session
        if 'page_visits' not in request.session:
            request.session['page_visits'] = {}

        page_visits = request.session['page_visits']
        page_key = 'home_page'

        # Increment visit count for this page
        page_visits[page_key] = page_visits.get(page_key, 0) + 1
        request.session['page_visits'] = page_visits
        request.session.modified = True

        return super().get(request, *args, **kwargs)


class AboutView(View):
    """Class-based view for about page."""
    template_name = 'post/about.html'

    def get(self, request):
        return render(request, template_name=self.template_name, context={'title': 'About'})


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


class UserPostsView(ListView):
    """Class-based view for displaying posts by a specific user."""
    model = Post
    template_name = 'post/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=self.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.user
        context['title'] = f"Posts by {self.user.get_full_name or self.user.username}"
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
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Track recently viewed posts in session
        if 'recently_viewed' not in request.session:
            request.session['recently_viewed'] = []

        recently_viewed = request.session['recently_viewed']
        post_id = str(self.object.id)

        # Remove if already in list and re-add to make it most recent
        if post_id in recently_viewed:
            recently_viewed.remove(post_id)
        recently_viewed.insert(0, post_id)

        # Keep only last 5 viewed posts
        request.session['recently_viewed'] = recently_viewed[:5]
        request.session.modified = True

        return response


class CreatePostView(LoginRequiredMixin, FormErrorMessagesMixin, CreateView):
    """Class-based view for creating a new blog post."""
    model = Post
    form_class = PostForm
    template_name = 'post/create_post.html'
    login_url = 'account:login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})


class EditPostView(LoginRequiredMixin, UserOwnsObjectMixin, FormErrorMessagesMixin, UpdateView):
    """Class-based view for editing an existing blog post."""
    model = Post
    form_class = PostForm
    template_name = 'post/edit_post.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    login_url = 'account:login'

    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})


class DeletePostView(LoginRequiredMixin, UserOwnsObjectMixin, DeleteView):
    """Class-based view for deleting a blog post."""
    model = Post
    template_name = 'post/delete_post.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('index')
    login_url = 'account:login'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CreateCommentView(LoginRequiredMixin, FormErrorMessagesMixin, View):
    """Class-based view for creating a comment on a post."""
    login_url = 'account:login'

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment posted successfully!')
        else:
            self.form_invalid(form)

        return redirect('post_detail', slug=post.slug)


class DeleteCommentView(LoginRequiredMixin, View):
    """Class-based view for deleting a comment."""
    login_url = 'account:login'

    def post(self, request, slug, comment_id):
        post = get_object_or_404(Post, slug=slug)
        comment = get_object_or_404(Comment, id=comment_id, post=post)

        if request.user != comment.author and request.user != post.author:
            messages.error(request, 'You can only delete your own comments.')
            return redirect('post_detail', slug=post.slug)

        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('post_detail', slug=post.slug)
