from rest_framework import serializers
from app import models

class UserModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        exclude = ("created_at", "updated_at")
        
class ProductListSerializers(serializers.ModelSerializer):
    contract = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    contract = serializers.StringRelatedField()
    class Meta:
        model = models.Product
        exclude = ("created_at", "updated_at")

    def get_contract(self, obj):
        return {'id': obj.contract.id, 'contract': str(obj.contract)}

    def get_user(self, obj):
        return {'id': obj.user.id, 'name': str(obj.user)}

    def get_category(self, obj):
        return {'id': obj.category.id, 'name': str(obj.category)}