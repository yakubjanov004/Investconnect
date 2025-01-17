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



class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name',)
        read_only = True



class ProductListSerializer(serializers.ModelSerializer):
    category = GetCategorySerializer(read_only=True)

    class Meta:
        model = models.Product_1
        fields = (
            'id', 'name', 'category', 'price', 'image'
        )


class ProductInforationNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('name',)
        read_only = True





class PrivateInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrivateInformation
        fields = ['kampanya_egasi', 'kontact', 'campany_name', 'oylik_daromadi', 'soff_foydasi']



class ProductCreateSerializer(serializers.ModelSerializer):
    private_information = PrivateInformationSerializer(read_only=True)  

    class Meta:
        model = models.Product
        fields = [
            'name', 'description', 'location', 'user', 'category',
            'rendement', 'image', 'price', 'product_file', 'private_information'
        ]

    def create(self, validated_data):
        private_info_data = validated_data.pop('private_information', None)

        product = models.Product.objects.create(**validated_data)

        if private_info_data:
            models.PrivateInformation.objects.create(product=product, **private_info_data)

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
        fields = ('username', 'firstname', 'lastname', 'profile_image', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields.pop('role', None)

    def validate_profile_image(self, value):
        if value and not value.name.endswith(('.jpg', '.png', '.jpeg',)):
            raise serializers.ValidationError("Only image files (jpg, png, jpeg) are allowed.")
        return value

    def update(self, instance, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        if profile_image:
            instance.profile_image = profile_image
        
        instance = super().update(instance, validated_data)
        instance.save()
        return instance



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
        model = models.Product_1
        fields = (
            'id', 'name', 'image', 'category', 'price', 'created_at' 
        )



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product_1
        fields = ['id', 'name', 'price', 'image', 'created_at' ]

                            # /////--------------------------------########/////---------------------#


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product_1
        fields = [
            'id', 
            'name', 
            'description', 
            'location', 
            'image', 
            'user', 
            'category', 
            'rendement', 
            'price', 
            'is_active',
            'short_description',  # Umumiy ma'lumotlar
            'investment_range',   # Kerakli sarmoya diapazoni
            'team_info',          # Jamoa haqida umumiy ma'lumot
            'business_plan',      # Batafsil biznes-reja
            'use_of_investment',  # Sarmoya foydalanish rejalari
            'financial_forecasts', # Moliyaviy prognozlar
            'prototype_demo',     # Prototip yoki demo
            'team_details',       # Jamoa a'zosining rezume va tajribasi
            'market_analysis',    # Bozor va raqobat tahlili
            'legal_documents',    # Yuridik hujjatlar
            'contact_info',       # Bog'lanish ma'lumotlari
        ]



# Serializer for open data
class ProductPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product_1
        fields = [
            'id',
            'name',
            'description',
            'location',
            'image',
            'price',
            'rendement',
            'short_description',
            'investment_range',
        ]

# Serializer for private data
class ProductPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product_1
        exclude = [
            'updated_at',
            'id',
            'name',
            'description',
            'location',
            'image',
            'price',
            'rendement',
            'short_description',
            'investment_range',
        ]