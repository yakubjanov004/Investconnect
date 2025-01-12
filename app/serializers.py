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
    images = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = (
            'id', 'name', 'category', 'price', 'image', 'images'
        )

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]




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
    product_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    product_file = serializers.FileField(allow_null=True, required=False)

    class Meta:
        model = models.Product
        fields = (
            'user', 'name', 'rendement', 'location', 'description', 'category', 'price', 'product_file', 'product_images'
        )

    def create(self, validated_data):
        product_images_data = validated_data.pop('product_images', [])
        product_file_data = validated_data.pop('product_file', None) 
        product = models.Product.objects.create(**validated_data)
        
        if product_file_data:
            product.product_file = product_file_data
            product.save()

        for image in product_images_data:
            models.ProductImage.objects.create(product=product, image=image)

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['role'] = instance.role  
        return representation

    def validate_profile_image(self, value):
        if value and not value.name.endswith(('.jpg', '.png', '.jpeg',)):
            raise serializers.ValidationError("Only image files (jpg, png, jpeg) are allowed.")
        return value

    def update(self, instance, validated_data):
        if 'role' in validated_data:
            raise serializers.ValidationError({"role": "Role maydoni o'zgartirilishi mumkin emas."})
        
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
        model = models.Product
        fields = (
            'id', 'name', 'degree','image','category', 'price'
        )

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'price', 'image']

