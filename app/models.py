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
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    rendement = models.CharField(max_length=5)
    image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_file = models.FileField(upload_to="product_file", blank=True, null=True)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class PrivateInformation(BaseModel):
    class DegreeChoicess(models.TextChoices):
        AKTIV = 'aktiv', 'Aktiv'
        DEAKTIV = 'deaktiv', 'Deaktiv'
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    status = models.CharField(max_length=30, choices=DegreeChoicess.choices, default=DegreeChoicess.AKTIV)
    kampanya_egasi = models.CharField(max_length=50)
    kontact = models.CharField(max_length=50)
    campany_name = models.CharField(max_length=50)
    oylik_daromadi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    soff_foydasi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.product.name}"




class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.product.name} | {self.user.username}: {self.description[:30]}..."


                            # /////--------------------------------########/////---------------------#


class Product_1(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="products/")
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    rendement = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=False)
    
    
    short_description = models.TextField(null=True, blank=True)  
    investment_range = models.CharField(max_length=100, null=True, blank=True)  
    team_info = models.TextField(null=True, blank=True)  

    
    business_plan = models.TextField(null=True, blank=True)  
    use_of_investment = models.TextField(null=True, blank=True)  
    financial_forecasts = models.TextField(null=True, blank=True) 
    prototype_demo = models.ImageField(upload_to="product_prototype/", null=True, blank=True)  
    team_details = models.TextField(null=True, blank=True)  
    market_analysis = models.TextField(null=True, blank=True)  
    legal_documents = models.FileField(upload_to="legal_docs/", null=True, blank=True)  
    contact_info = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.name
    
class Payment(models.Model):
    investor = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_1, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)  

    def __str__(self):
        return f"Payment for {self.product.name} by {self.investor.username} - ${self.amount}"