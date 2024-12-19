from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.core import validators

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

@deconstructible
class UnicodePhoneValidator(validators.RegexValidator):
    regex = r"^\+998\d{9}$"
    message = _(
        "Yaroqli telefon raqamini kiriting. Format: +998XXXXXXXXX (aniq 13 ta belgi)."
    )
    flags = 0
phone_validator = UnicodePhoneValidator()
class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError(_('The Phone field must be set'))
        phone = self.normalize_phone(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone, password, **extra_fields)

    def normalize_phone(self, phone):
        return phone
class UserModel(AbstractUser):
    class RoleChoicess(models.TextChoices):
        INVESTOR = 'investor', 'Investor'
        STARTUP = 'startup', 'Startup'
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    role = models.CharField(max_length=30, choices=RoleChoicess.choices)
    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        help_text=_("Majburiy. Username faqat harflar va raqamlardan iborat bo'lishi kerak."),
        error_messages={
        "unique": _("Bu username ga ega foydalanuvchi allaqachon mavjud."),
    },
)

    phone = models.CharField(
        _("phone"),
        max_length=13,  
        unique=True,
        help_text=_("Majburiy. Format: +998XXXXXXXXX."),
        validators=[phone_validator],  
        error_messages={
        "unique": _("Bu telefon raqamiga ega foydalanuvchi allaqachon mavjud."),
    },
)
    class UserAuthStatus(models.TextChoices):
        NEW = "new", "Yangi"
        APPROVED = "approwed", "Tasdiqlangan"
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
 
    objects = CustomUserManager()
    status = models.CharField(
        max_length=100,
        choices=UserAuthStatus.choices,
          default=UserAuthStatus.NEW
    )
    code = models.CharField(max_length=6, null=True)  
    expire_date = models.DateTimeField(null=True)
    def generate_verification_code(self):
        from datetime import datetime, timedelta
        import random
        self.code = ''.join([str(random.randint(0, 9)) for _ in range(6)])  
        self.expire_date = datetime.now() + timedelta(minutes=1)
    

    def __str__(self):
        return f"{self.id}- {self.username} - {self.firstname} - {self.lastname}"

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