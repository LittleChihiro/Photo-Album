import profile
from django.urls import path
from . import views
from .views import loginUser
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
    
    path('login/', loginUser, name='login'),
    path('signup/', views.signup, name='signup'),
    
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile, name='profile'),
    ]