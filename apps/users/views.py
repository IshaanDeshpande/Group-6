from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import LoginForm, ProfileForm, SignUpForm
from .models import Profile


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            Profile.objects.create(user=user, zip_code=form.cleaned_data['zip_code'])
            auth_login(request, user)
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                auth_login(request, user)
                return redirect('core:home')
            form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'delete_account' in request.POST:
            user = request.user
            auth_logout(request)
            user.delete()
            return redirect('core:home')

        form = ProfileForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            if form.cleaned_data['password']:
                request.user.set_password(form.cleaned_data['password'])
            request.user.save()
            profile_obj.zip_code = form.cleaned_data['zip_code']
            profile_obj.save()
            if form.cleaned_data['password']:
                update_session_auth_hash(request, request.user)
            return redirect('users:profile')
    else:
        form = ProfileForm(user=request.user, initial={
            'username': request.user.username,
            'email': request.user.email,
            'zip_code': profile_obj.zip_code,
        })
    return render(request, 'users/profile.html', {'form': form})
