from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserModel
from app import models
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
        fields = (
            'contract',
        )

class GetUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserModel
        fields = (
            'firstname',
            'lastname',
            'role',
        )

class GetCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = (
            'name',
        )
        
class ProductListSerializers(serializers.ModelSerializer):
    user = GetUserSerializer()
    contract = ContractNameSerializer()
    category = GetCategorySerializer()
    class Meta:
        model = models.Product
        exclude = ("created_at", "updated_at")

######## COMMENT

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        exclude = ("created_at", "updated_at")

class CreatProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        exclude = ("created_at", "updated_at")

class RegistrSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        exclude = ("created_at", "updated_at")

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = (
            'firstname',
            'lastname',
            'phone',
            )