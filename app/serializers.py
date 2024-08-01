from rest_framework import serializers
from app import models
######## USER
class UserModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        exclude = ("created_at", "updated_at")

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