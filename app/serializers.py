from rest_framework import serializers
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
        fields = ('firstname', 'lastname', 'phonenumber')
