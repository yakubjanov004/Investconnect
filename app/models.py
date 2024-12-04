from django.db import models
from django.core.validators import RegexValidator


# BaseModel - barcha modellar uchun umumiy maydonlar
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


# UserModel - foydalanuvchilar uchun model
class UserModel(BaseModel):
    class RoleChoices(models.TextChoices):
        INVESTOR = 'investor', 'Investor'
        CREATOR = 'creator', 'Creator'

    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=50)
    phonenumber = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")],
    )
    email = models.EmailField(unique=True)  # Unikal email
    role = models.CharField(max_length=30, choices=RoleChoices.choices)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


# Contract - foydalanuvchilar bilan tuzilgan shartnomalar
class Contract(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='contracts')
    contract = models.TextField(verbose_name='Contract Details')

    def __str__(self):
        return f"Contract with {self.user.firstname}"


# Category - mahsulotlar uchun kategoriyalar
class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Product - foydalanuvchilar mahsulotlari
class Product(BaseModel):
    class DegreeChoices(models.TextChoices):
        BRONZE = 'bronze', 'Bronze'
        SILVER = 'silver', 'Silver'
        GOLD = 'gold', 'Gold'

    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    degree = models.CharField(max_length=30, choices=DegreeChoices.choices, default=DegreeChoices.BRONZE)
    description = models.TextField()
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, related_name='products')

    def __str__(self):
        return self.name


# Information - mahsulot haqida qo'shimcha ma'lumotlar
class Information(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='information')
    key = models.CharField(max_length=100)  # Kengroq maydon
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.key}: {self.value}"


# Comment - mahsulotlar uchun foydalanuvchi izohlari
class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='comments')
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='comments')
    description = models.TextField()

    class Meta:
        unique_together = ('product', 'user')  # Har bir foydalanuvchi faqat bitta izoh qoldirishi mumkin

    def __str__(self):
        return f"Comment by {self.user.firstname} on {self.product.name}"
