# Generated by Django 5.0.7 on 2025-01-04 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_usermodel_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='image',
            new_name='profile_image',
        ),
    ]
