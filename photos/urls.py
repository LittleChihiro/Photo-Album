from django.urls import path
from .views import home, gallery, viewPhoto, addPhoto, loginUser, profile, edit_profile, change_photo_status
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),  # Home-Seite als die Standardseite
    path('gallery/', gallery, name='gallery'),
    path('photo/<str:pk>', viewPhoto, name='photo'),
    path('add/', addPhoto, name='add'),
    path('login/', loginUser, name='login'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('photo/change-status/<int:photo_id>/', change_photo_status, name='change_photo_status'),
]
