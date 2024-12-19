from django.db import models
from userapp.models import UserModel  
from userapp.base import BaseModel  


class Contract(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    contract = models.TextField()

    def __str__(self):
        return f"User ID: {self.user.id} | Contract ID: {self.id}"


class Category(BaseModel):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to="category/", null=True, blank=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    class DegreeChoicess(models.TextChoices):
        BRONZE = 'bronze', 'Bronze'
        SILVER = 'silver', 'Silver'
        GOLD = 'gold', 'Gold'

    name = models.CharField(max_length=50)
    degree = models.CharField(max_length=30, choices=DegreeChoicess.choices, default=DegreeChoicess.BRONZE)
    description = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="products/")
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    rendement = models.CharField(max_length=5)
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class Information(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product.name} | {self.key}: {self.value}"


class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    description = models.TextField()

    def __str__(self):
        return f"{self.product.name} | {self.user.username}: {self.description[:30]}..."
