from django.urls import path
from .views import home, gallery, logoutUser, viewPhoto, addPhoto, loginUser, profile, edit_profile, change_photo_status
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from photos import views

urlpatterns = [
    path('', home, name='home'),  # Home-Seite als die Standardseite
    path('gallery/', gallery, name='gallery'),
    path('photo/<str:pk>', viewPhoto, name='photo'),
    path('add/', addPhoto, name='add'),
    path('login/', loginUser, name='login'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('logout/',logoutUser , name='logout'),     
    path('photo/change-status/<int:photo_id>/', change_photo_status, name='change_photo_status'),
    path('photo/delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
