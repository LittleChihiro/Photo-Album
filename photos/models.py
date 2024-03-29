from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_standard = models.BooleanField(default=False)  # Feld für Standardkategorien
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Feld für Benutzer

    def __str__(self):
        return self.name
    
class Photo(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)    
    
    def __str__(self):
        return self.description
    
    name = models.CharField(max_length=255)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    size = models.FloatField(null=True, blank=True)  # In Megabytes
    format = models.CharField(max_length=10, null=True, blank=True)
    copyright = models.CharField(max_length=255, blank=True, null=True)
    source = models.URLField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='photos_created', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='photos_updated', on_delete=models.SET_NULL, null=True)
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('approved', 'Approved'),
        ('optimized', 'Optimized'),
        ('locked', 'Locked'),
        ('standard', 'Standard'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
