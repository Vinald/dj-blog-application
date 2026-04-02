from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm


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


@require_http_methods(["GET", "POST"])
@login_required
def edit_profile(request):
    """Handle user profile editing with form validation."""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('account:profile')
        else:
            if user_form.errors:
                for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
            if profile_form.errors:
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/edit_profile.html', context)

