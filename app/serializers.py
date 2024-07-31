from rest_framework import serializers
from app import models

class UserModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = '__all__'
        
