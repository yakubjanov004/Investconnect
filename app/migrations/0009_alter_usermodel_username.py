# Generated by Django 5.0.7 on 2024-12-16 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='username',
            field=models.CharField(error_messages={'unique': 'Bu username ga ega foydalanuvchi allaqachon mavjud.'}, help_text="Majburiy. Username faqat harflar va raqamlardan iborat bo'lishi kerak.", max_length=30, unique=True, verbose_name='username'),
        ),
    ]
