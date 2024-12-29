from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserModel
from app import models
from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ('id', 'firstname', 'phone', 'lastname', 'email', 'role')

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ('firstname', 'lastname', 'role')
        read_only = True

class Userserializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, validators=[ 
        RegexValidator(
            regex=r'^[a-zA-Z0-9]+$', 
            message="Username faqat harflar va raqamlardan iborat bo'lishi kerak."
        ),
    ])
    phone = serializers.CharField(validators=[
        RegexValidator(
            regex=r"^\+998\d{9}$",
            message="Telefon raqam formati noto‘g‘ri. Format: +998XXXXXXXXX"
        )
    ])
    role = serializers.CharField(max_length=35)
    password = serializers.CharField(write_only=True)


class VerifySerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.filter(status='new'))
    code = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        if not phone or not password:
            raise ValidationError({"error": "Telefon raqam va parolni kiriting."})

        user = authenticate(request=self.context.get('request'), username=phone, password=password)
        if not user:
            raise ValidationError({"error": "Notog'ri telefon raqam yoki parol."})

        data['user'] = user
        return data



class ContractNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contract
        fields = ('contract',)
        read_only = True



class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name',)
        read_only = True



class ProductListSerializer(serializers.ModelSerializer):
    # user = GetUserSerializer(read_only=True)
    # contract = ContractNameSerializer(read_only=True)
    category = GetCategorySerializer(read_only=True)

    class Meta:
        model = models.Product
        fields = (
            'id', 'name', 'degree','image','category', 'price'
        )

class ProductInforationNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('name',)
        read_only = True

class ProductinformationSerializer(serializers.ModelSerializer):
    product = ProductInforationNameSerializer(read_only=True)

    class Meta:
        model = models.PrivateInformation
        exclude = ('created_at',  'updated_at')



class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('user','name', 'rendement','location', 'image', 'description', 'category', 'contract', 'price')



class CommentSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)  

    class Meta:
        model = models.Comment
        fields = ('id', 'description', 'user', 'product')



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ('firstname', 'lastname', 'phone', 'email', 'role')



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('firstname', 'lastname', 'phone',)


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"



class ProfilDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username','firstname', 'lastname', 'phone', 'email', 'role')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', "img"]

class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrivateInformation
        exclude = ('created_at',  'updated_at')


class UserProductSerializer(serializers.ModelSerializer):
    category = GetCategorySerializer(read_only=True)

    class Meta:
        model = models.Product
        fields = (
            'id', 'name', 'degree','image','category', 'price'
        )
