# Generated by Django 5.0.7 on 2024-12-12 16:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_usermodel_code_alter_usermodel_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='username',
            field=models.CharField(blank=True, max_length=35, unique=True, validators=[django.core.validators.RegexValidator(message='Username faqat lotin harflari va raqamlardan iborat bo‘lishi kerak. Joy tashlashga ruxsat yo‘q.', regex='^[A-Za-z0-9]+$')]),
        ),
    ]