from django.urls import path
from . import views
from .views import loginUser

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
    
    path('login/', loginUser, name='login'),
    path('signup/', views.signup, name='signup'),
]