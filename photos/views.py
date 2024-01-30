from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from PIL import Image, ExifTags


# Create your views here.

def gallery(request):
    category = request.GET.get('category')

    # Fotos aus der Standardkategorie
    standard_photos = Photo.objects.filter(category__is_standard=True)

    if request.user.is_superuser:
        # Wenn der Benutzer ein Superuser ist, zeige alle Fotos
        photos = Photo.objects.all()
    elif request.user.is_authenticated:
        # Fotos des Benutzers und der Standardkategorie
        user_photos = Photo.objects.filter(user=request.user)
        photos = user_photos | standard_photos
    else:
        # Nur Fotos der Standardkategorie für nicht eingeloggte Benutzer
        photos = standard_photos

    # Filtern der Fotos, wenn eine spezifische Kategorie ausgewählt wurde
    if category is not None:
        photos = photos.filter(category__name__contains=category)

    categories = Category.objects.all()
    
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


def get_image_info(image):
    with Image.open(image) as img:
        width, height = img.size
        format = img.format
        size = round(image.size / (1024 * 1024), 2)  # Größe in MB

        # Versuch, Exif-Daten zu extrahieren
        exif_data = {}
        if hasattr(img, '_getexif'):
            exif = img._getexif()
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
            
            Photo = Photo.objects.create(
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


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'photos/signup.html', {'form': form})

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