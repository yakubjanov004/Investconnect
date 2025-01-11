from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserModel
from app import models
from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.files.base import ContentFile
import requests
import os


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
            'id', 'name','image','category', 'price'
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

class PrivateInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrivateInformation
        fields = ('kampanya_egasi', 'kontact', 'campany_name', 'oylik_daromadi', 'soff_foydasi')


class CreateProductSerializer(serializers.ModelSerializer):
    private_information = PrivateInformationSerializer()

    class Meta:
        model = models.Product
        fields = (
            'user', 'name', 'rendement', 'location', 'image',
            'description', 'category','price',
            'private_information'
        )

    def create(self, validated_data):
        private_information_data = validated_data.pop('private_information', None)
        product = models.Product.objects.create(**validated_data)
        if private_information_data:
            private_info = models.PrivateInformation.objects.create(product=product, **private_information_data)
            product.private_information = private_info
        return product


class CommentSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)  

    class Meta:
        model = models.Comment
        fields = ('id', 'description', 'user', 'product')




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
        fields = ('username', 'firstname', 'lastname', 'profile_image', 'phone', 'email', 'role')

    def validate_profile_image(self, value):
        if isinstance(value, str) and value.startswith('http'):  
            response = requests.get(value)
            if response.status_code != 200:
                raise serializers.ValidationError("The URL is not accessible.")
        elif value and not value.name.endswith(('.jpg', '.png', '.jpeg')):
            raise serializers.ValidationError("Only image files (jpg, png, jpeg) are allowed.")
        return value

    def update(self, instance, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        if profile_image:
            if isinstance(profile_image, str) and profile_image.startswith('http'):  
                response = requests.get(profile_image)
                if response.status_code == 200:
                    file_name = os.path.basename(profile_image)
                    instance.profile_image.save(file_name, ContentFile(response.content), save=False)
            else:
                instance.profile_image = profile_image
        instance = super().update(instance, validated_data)
        instance.save()
        return instance

CreateProductSerializer

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
