from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm, LoginForm


@require_http_methods(["GET", "POST"])
def register(request):
    """Handle user registration with form validation and error handling."""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                'Account successfully created! Please log in.'
            )
            return redirect('account:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()

    return render(request, 'account/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login with secure authentication."""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            # Redirect to next page if provided, otherwise to index
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Handle user logout with confirmation."""
    if not request.user.is_authenticated:
        messages.warning(request, 'You are not logged in.')
        return redirect('account:login')

    if request.method == 'POST':
        user_username = request.user.username
        logout(request)
        messages.success(request, f'Goodbye {user_username}! You have been logged out.')
        return redirect('index')

    # GET request - show logout confirmation page
    return render(request, 'account/logout.html')


@require_http_methods(["GET"])
@login_required
def profile(request):
    """Display user profile information."""
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to log in to view your profile.')
        return redirect('account:login')

    return render(request, 'account/profile.html', {'user': request.user})
