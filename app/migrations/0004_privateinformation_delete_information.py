# Generated by Django 5.0.7 on 2024-12-29 07:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(choices=[('aktiv', 'Aktiv'), ('deaktiv', 'Deaktiv')], default='aktiv', max_length=30)),
                ('kampanya_egasi', models.CharField(max_length=50)),
                ('kontact', models.CharField(max_length=50)),
                ('campany_name', models.CharField(max_length=50)),
                ('oylik_daromadi', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('soff_foydasi', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Information',
        ),
    ]
