import os
from unicodedata import category
from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib import messages, auth
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from PIL import Image, ExifTags

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect

from django.contrib.auth.models import User
import random


def gallery(request):
    categories = Category.objects.all().order_by('name')
    pitphotos_category = categories.filter(name='PitPhotos').first()

    if request.user.is_authenticated:
        if request.user.is_superuser:
            photos = Photo.objects.all()  # Admins see all photos
        else:
            user_photos = Photo.objects.filter(user=request.user)
            pitphotos = Photo.objects.filter(category=pitphotos_category)
            photos = user_photos | pitphotos
    else:
        photos = Photo.objects.filter(category=pitphotos_category)

    # filtering for all users
    query = request.GET.get('query')
    sort = request.GET.get('sort')
    status = request.GET.get('status')
    category_name = request.GET.get('category')

    if query:
        photos = photos.filter(description__icontains=query)
    if status:
        photos = photos.filter(status=status)
    if category_name:
        photos = photos.filter(category__name=category_name)
    if sort == 'latest':
        photos = photos.order_by('-created_at')

    context = {'categories': categories, 'photos': photos.distinct()}
    return render(request, 'photos/gallery.html', context)


def get_image_info(image):
    size = round(len(image) / 1024.0, 3)  # KB
    with Image.open(image) as img:
        width, height = img.size
        format = img.format

        exif_data = {}
        exif = img.getexif()  
        if exif is not None:
            for tag, value in exif.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                exif_data[decoded] = value

    return width, height, format, size, exif_data


def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})

def addPhoto(request):
    categories = Category.objects.exclude(name="PitPhotos") if not request.user.is_superuser else Category.objects.all()
    
    if request.method == 'POST':
        if 'category' in request.POST and request.POST['category'] == str(Category.objects.get(name="PitPhotos").id):
            if not request.user.is_superuser:
                return HttpResponseForbidden("Only admins are allowed to add images to the PitPhotos category.")
            
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        for image in images:
            width, height, format, size, exif_data = get_image_info(image)
            photo = Photo.objects.create(
                name=data.get('name'),
                category=category,
                description=data['description'],
                image=image,
                user=request.user,
                width=width,
                height=height,
                format=format,
                size=size,
                copyright=data.get('copyright'),
                source=data.get('source'),
                created_by=request.user,
                updated_by=request.user,
            )

        # Weiterleitung zur Galerie-Seite nach dem Speichern der Bilder
        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)


def delete_photo(request, photo_id):
    if request.method == 'POST':
        photo = get_object_or_404(Photo, id=photo_id)
        photo.delete()
        return redirect('gallery')
    else:
        return redirect('photo', photo_id=photo_id)
    
    
def change_photo_status(request, photo_id):
        photo = get_object_or_404(Photo, pk=photo_id)
        if request.user != photo.user and not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to change the status of this photo.")

        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in dict(Photo.STATUS_CHOICES).keys():
                photo.status = new_status
                photo.save()
                return redirect('gallery') 
            else:
                return HttpResponseForbidden("Invalid status option.")


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('gallery')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'photos/login.html')


def profile(request):
    return render(request, 'photos/profile.html')

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        try:
            user.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Error updating profile: {e}')

    return render(request, 'photos/edit_profile.html', {'user': user})

def logoutUser(request):
    global userid
    auth.logout(request) 
    return HttpResponseRedirect("/login/")


def home(request):
    try:
        pitphotos_category = Category.objects.get(name='PitPhotos')
        photos = Photo.objects.filter(category=pitphotos_category)
        if photos.exists():
            random_photos = random.sample(list(photos), k=min(9, len(photos))) 
            grouped_photos = [random_photos[i:i + 3] for i in range(0, len(random_photos), 3)] 
        else:
            grouped_photos = []
    except Category.DoesNotExist:
        grouped_photos = []

    context = {'grouped_photos': grouped_photos}
    return render(request, 'photos/home.html', context)