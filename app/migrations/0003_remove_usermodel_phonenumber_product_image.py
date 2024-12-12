# Generated by Django 5.0.7 on 2024-12-12 15:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_comment_description_usermodel_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='phonenumber',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='products/'),
            preserve_default=False,
        ),
    ]