from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.core import validators
from django.core.validators import RegexValidator


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

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



class UserModel(BaseModel):
    class RoleChoices(models.TextChoices):
        INVESTOR = 'investor', 'Investor'
        CREATOR = 'creator', 'Creator'
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=50)
    username = None
    email = models.EmailField()
    role = models.CharField(max_length=30, choices=RoleChoices.choices)
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
    code = models.CharField(max_length=4, null=True)
    expire_date = models.DateTimeField(null=True)

    def generate_verification_code(self):
            from datetime import datetime, timedelta
            import random
            self.code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            self.expire_date = datetime.now() + timedelta(minutes=1)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
    
    phonenumber = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")],
    )
    email = models.EmailField(unique=True) 
    role = models.CharField(max_length=30, choices=RoleChoices.choices)

    def __str__(self):
        return f"{self.id} - {self.firstname}"



class Contract(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='contracts')
    contract = models.TextField(verbose_name='Contract Details')

    def __str__(self):
        return f"Contract with {self.user.firstname}"



class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



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



class Information(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='information')
    key = models.CharField(max_length=100) 
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.key}: {self.value}"



class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='comments')
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='comments')
    description = models.TextField()

    class Meta:
        unique_together = ('product', 'user') 

    def __str__(self):
        return f"Comment by {self.user.firstname} on {self.product.name}" 