from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.


def gallery(request):
    category = request.GET.get('category')

    if request.user.is_superuser:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(user=request.user)

    if category is not None:
        photos = photos.filter(category__name__contains=category)
      
    categories = Category.objects.all()      
    
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


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
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
                user=request.user  # Hinzufügen des aktuellen Benutzers
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
            return redirect('login')  # Oder eine andere Seite nach der Registrierung
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
            # Redirect to the profile page
            return redirect('profile')  # Stelle sicher, dass du eine URL mit dem Namen 'profile' hast
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, 'photos/edit_profile.html', {'form': form})


def home(request):
    return render(request, 'photos/home.html')