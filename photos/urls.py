import profile
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import home, gallery, viewPhoto, addPhoto, loginUser, signup, profile, edit_profile

urlpatterns = [
    path('', home, name='home'),  # Home-Seite als die Standardseite
    path('gallery/', gallery, name='gallery'),
    path('photo/<str:pk>', viewPhoto, name='photo'),
    path('add/', addPhoto, name='add'),
    path('login/', loginUser, name='login'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    
]