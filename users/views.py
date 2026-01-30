from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm, RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("/")
        messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
        messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("/")


@login_required
def profile_view(request, username=None):
    from django.contrib.auth.models import User
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    from posts.models import Post
    posts = Post.objects.filter(author=user).order_by("-created_at")[:20]
    return render(request, "users/profile.html", {"profile_user": user, "profile": profile, "posts": posts})


@login_required
def profile_edit_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("users:profile", username=request.user.username)
        messages.error(request, "Please fix the errors.")
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "users/profile_edit.html", {"form": form})
