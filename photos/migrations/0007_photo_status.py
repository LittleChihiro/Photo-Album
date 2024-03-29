# Generated by Django 5.0 on 2024-02-07 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0006_photo_copyright_photo_created_at_photo_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('approved', 'Approved'), ('edited', 'Edited'), ('optimized', 'Optimized'), ('locked', 'Locked')], default='new', max_length=10),
        ),
    ]
