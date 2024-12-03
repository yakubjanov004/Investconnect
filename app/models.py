from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class UserModel(BaseModel):
    class RoleChoicess(models.TextChoices):
        INVESTOR = 'investor', 'Investor'
        CREATOR = 'creator', 'Creator'

    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=15) 
    email = models.EmailField()
    role = models.CharField(max_length=30, choices=RoleChoicess.choices)

    def __str__(self):
        return self.firstname

class Contract(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    contract = models.TextField()


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(BaseModel):
    class DegreeChoicess(models.TextChoices):
        BRONZE = 'bronze', 'Bronze'
        SILVER = 'silver', 'Silver'
        GOLD = 'gold', 'Gold'
    
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    degree = models.CharField(max_length=30, choices=DegreeChoicess.choices, default=DegreeChoicess.BRONZE)
    description = models.TextField()
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Information(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    description = models.TextField()