from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login as auth_login , logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import *
from .models import *

# --- Authentication views ---
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
            messages.error(" Invalid username or password. ")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})
            
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('login')

@login_required
def update_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile', request.user.id)
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def profile(request, user_id): # View for user profile
    user = get_object_or_404(User, id=user_id)
    profile = UserProfile.objects.filter(user=user).first()
    if not profile:
        profile = UserProfile(user=user)
    return render(request, 'profile.html', {'profile': profile})


def home(request): # Home Page View
    artworks = Artwork.objects.all()
    categories = Catogories.objects.all()
    tags = Tags.objects.all()
    return render(request, 'home.html', {'artworks': artworks,'categories':categories, 'tags':tags})

@login_required # View For to like a artwork
def like_artwork(request, artwork_id):
    artwork = Artwork.objects.get(id=artwork_id)
    if artwork.likes:
        artwork.likes -=1
    else:
        artwork.likes +=1
    artwork.save()
    return JsonResponse({'likes': artwork.likes})


@login_required # View For to like a comment
def like_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    # Toggle the like count for the comment
    if comment.likes:
        comment.likes -= 1
    else:
        comment.likes += 1
    comment.save()
    return JsonResponse({'likes': comment.likes})

def filter_artwork(request, category_name=None, tag_name=None): # To filter the artworks based on category and tag
    artworks = Artwork.objects.all()
    if category_name:
        artworks = artworks.filter(catogories__name = category_name)
    if tag_name:
        artworks= artworks.filter(tags__name = tag_name)
    
    categories = Catogories.objects.all()
    tags = Tags.objects.all()   
    return render(request, 'home.html', {'artworks': artworks, 'categories':categories,'tags':tags})


@login_required 
def upload_artwork(request): # To upload a artwork to the forum
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.created_by = request.user
            artwork.save()
            form.save_m2m()
            messages.success(request, 'Artwork uploaded successfully')
            return redirect('home')
    else:
        form = ArtworkForm()
    return render(request, 'upload_artwork.html', {'form': form})

@login_required
def add_comment(request, artwork_id): #  To add a comment to an art
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.artwork_id = artwork_id
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully')
            return redirect('art', artwork_id)
    return redirect('art', artwork_id)
