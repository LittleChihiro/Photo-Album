import os
from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from PIL import Image, ExifTags

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden


def gallery(request):
    category = request.GET.get('category')
    query = request.GET.get('query')

    if request.user.is_superuser:
        photos = Photo.objects.all()
    elif request.user.is_authenticated:
        photos = Photo.objects.filter(user=request.user) | Photo.objects.filter(category__is_standard=True)
    else:
        photos = Photo.objects.filter(category__is_standard=True)

    if category:
        photos = photos.filter(category__name__contains=category)

    if query:
        photos = photos.filter(description__icontains=query)

    categories = Category.objects.all()
    
    context = {'categories': categories, 'photos': photos}
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
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                name=data['category_new'])
        else:
            category = None

        for image in images:
            width, height, format, size, exif_data = get_image_info(image)
    
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
                user=request.user, 
                width=width,
                height=height,
                format=format,
                size=size,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)

def change_photo_status(request, photo_id):
        photo = get_object_or_404(Photo, pk=photo_id)
        if request.user != photo.user and not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to change the status of this photo.")

        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in dict(Photo.STATUS_CHOICES).keys():
                photo.status = new_status
                photo.save()
                # Hier sollten Sie entscheiden, wohin der Benutzer nach der Änderung umgeleitet wird
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

def edit_profile(request):
    
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, 'photos/edit_profile.html', {'form': form})


def home(request):
    return render(request, 'photos/home.html')