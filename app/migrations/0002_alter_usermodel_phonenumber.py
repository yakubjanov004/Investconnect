# Generated by Django 5.0.7 on 2024-07-31 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='phonenumber',
            field=models.CharField(max_length=15),
        ),
    ]
