from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
# Add require_POST to protect our favorite submission route
from django.views.decorators.http import require_POST 

from .forms import LoginForm, ProfileForm, SignUpForm
# Import the new FavoriteResource model alongside Profile
from .models import Profile, FavoriteResource 


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
            
            # Log the user in automatically
            auth_login(request, user)
            
            # KEEP THEM SIGNED IN
            request.session.set_expiry(0)
            
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
                
                # KEEP THEM SIGNED IN ON LOGIN TOO
                request.session.set_expiry(0)
                
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
        
    # --- UPDATE HERE: Fetch the user's saved favorites ---
    favorites = request.user.favorites.all().order_by('-created_at')
        
    # Add favorites to the context dictionary
    return render(request, 'users/profile.html', {
        'form': form,
        'favorites': favorites
    })


# --- NEW VIEW: Handle saving the favorited item ---
@login_required
@require_POST
def add_to_favorites(request):
    FavoriteResource.objects.get_or_create(
        user=request.user,
        name=request.POST.get('name'),
        agency_name=request.POST.get('agency_name'),
        description=request.POST.get('description'),
        address=request.POST.get('address'),
        phone=request.POST.get('phone'),
        website=request.POST.get('website'),
    )
    # Redirect right back to the exact search results page they were looking at
    return redirect(request.META.get('HTTP_REFERER', 'resources:find_resources'))

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from .models import FavoriteResource  # Double check if your model is named FavoriteResource or similar

@login_required
@require_POST
def add_to_favorites(request):
    name = request.POST.get('name')
    agency_name = request.POST.get('agency_name', '')
    description = request.POST.get('description', '')
    address = request.POST.get('address', '')
    phone = request.POST.get('phone', '')
    website = request.POST.get('website', '')
    
    # This prevents creating duplicate favorites for the same user
    FavoriteResource.objects.get_or_create(
        user=request.user,
        name=name,
        defaults={
            'agency_name': agency_name,
            'description': description,
            'address': address,
            'phone': phone,
            'website': website,
        }
    )
    return redirect(request.META.get('HTTP_REFERER', 'users:profile'))

@login_required
@require_POST
def remove_from_favorites(request):
    resource_name = request.POST.get('name')
    FavoriteResource.objects.filter(user=request.user, name=resource_name).delete()
    return redirect(request.META.get('HTTP_REFERER', 'users:profile'))