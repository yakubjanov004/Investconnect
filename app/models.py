from django.db import models
from userapp.models import UserModel
from userapp.base import BaseModel



class Category(BaseModel):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to="category/", null=True, blank=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="products/")
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    rendement = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class PrivateInformation(BaseModel):
    class DegreeChoicess(models.TextChoices):
        AKTIV = 'aktiv', 'Aktiv'
        DEAKTIV = 'deaktiv', 'Deaktiv'
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=30, choices=DegreeChoicess.choices, default=DegreeChoicess.AKTIV)
    kampanya_egasi = models.CharField(max_length=50)
    kontact = models.CharField(max_length=50)
    campany_name = models.CharField(max_length=50)
    oylik_daromadi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    soff_foydasi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.product.name} | {self.key}: {self.value}"


class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.product.name} | {self.user.username}: {self.description[:30]}..."
