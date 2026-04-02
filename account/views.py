from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.utils.decorators import method_decorator

from .forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


class RegisterView(View):
    """Class-based view for user registration."""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')

        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account successfully created! Please log in.')
            return redirect('account:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return render(request, 'account/register.html', {'form': form})


class LoginView(DjangoLoginView):
    """Class-based view for user login using Django's built-in LoginView."""
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome back, {self.request.user.username}!')
        return response

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)


class LogoutView(View):
    """Class-based view for user logout with confirmation."""

    @method_decorator(login_required(login_url='account:login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'account/logout.html')

    def post(self, request):
        user_username = request.user.username
        logout(request)
        messages.success(request, f'Goodbye {user_username}! You have been logged out.')
        return redirect('index')


class ProfileView(LoginRequiredMixin, DetailView):
    """Class-based view for displaying user profile."""
    model = Profile
    template_name = 'account/profile.html'
    context_object_name = 'profile'
    login_url = 'account:login'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class EditProfileView(LoginRequiredMixin, View):
    """Class-based view for editing user profile."""
    login_url = 'account:login'
    template_name = 'account/edit_profile.html'

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
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

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)
