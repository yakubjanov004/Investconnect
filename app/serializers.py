from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserModel
from app import models


# Base User Serializer
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ('id', 'firstname', 'lastname', 'phonenumber', 'email', 'role')


# Nested User Serializer for Read-only
class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ('firstname', 'lastname', 'role')
        read_only = True


# Contract Serializer
from django.core.validators import RegexValidator
from app.models import phone_validator 

######## USER
class Userserializer(serializers.Serializer):
    phone = serializers.CharField(validators=[
        RegexValidator(
            regex=r"^\+998\d{9}$",
            message="Telefon raqam formati noto‘g‘ri. Format: +998XXXXXXXXX"
        )
    ])
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

        if phone and password:
            user = authenticate(request=self.context.get('request'), phone=phone, password=password)
            if not user:
                raise serializers.ValidationError({"error": "Notog'ri telefon raqam yoki parol."})
        else:
            raise serializers.ValidationError({"error": "Telefon raqam va parolni kiriting."})

        data['user'] = user
        return data
######## PRODUCT
class ContractNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contract
        fields = ('contract',)
        read_only = True


# Category Serializer
class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name',)
        read_only = True


# Product List Serializer (Nested)
class ProductListSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    contract = ContractNameSerializer(read_only=True)
    category = GetCategorySerializer(read_only=True)

    class Meta:
        model = models.Product
        fields = (
            'id', 'name', 'degree', 'description', 'user', 'contract', 'category'
        )


# Create Product Serializer
class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('user','name', 'degree', 'description', 'category', 'contract')


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)  # Nested User Serializer for Read-only

    class Meta:
        model = models.Comment
        fields = ('id', 'description', 'user', 'product')


# User Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ('firstname', 'lastname', 'phonenumber', 'email', 'role')


# User Update Serializer
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = (
            'firstname',
            'lastname',
            'phone',
            )