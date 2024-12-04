from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView, 
    RetrieveAPIView, 
    RetrieveUpdateAPIView
)
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from app import serializers, models


# User List API
class UserModelListAPIView(ListAPIView):
    serializer_class = serializers.UserModelSerializer
    queryset = models.UserModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only uchun ochiq

from django.contrib.auth.models import AnonymousUser
from app.models import Product, UserModel

class ProductListAPIView(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ('degree',)
    search_fields = ('name',)

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            # Handle anonymous users by returning no products or all products, as per your requirement
            return Product.objects.none()  # Or return all products if needed
        try:
            # Ensure that the user is a valid UserModel instance
            user_instance = UserModel.objects.get(id=user.id)
            return Product.objects.filter(user=user_instance)
        except UserModel.DoesNotExist:
            return Product.objects.none()


# Comment List API
class CommentListAPIView(ListAPIView):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        # Mahsulot bo'yicha izohlarni filtrlash
        product_id = self.request.query_params.get('product_id')
        if product_id:
            return models.Comment.objects.filter(product_id=product_id)
        return models.Comment.objects.all()


# Product Create API
class ProductCreateAPIView(CreateAPIView):
    serializer_class = serializers.CreateProductSerializer
    queryset = models.Product.objects.all()

    # def perform_create(self, serializer):
    #     # Avtomatik ravishda foydalanuvchini o‘rnatish
    #     serializer.save(user=self.request.user)





# User Registration API
class RegistrCreateAPIView(CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    queryset = models.UserModel.objects.all()


# User Update API
class UserUpdateAPIView(UpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    queryset = models.UserModel.objects.all()

    def get_object(self):
        # Foydalanuvchini o'ziga tegishli ma'lumotlarini o'zgartirishga majbur qilish
        return get_object_or_404(models.UserModel, id=self.request.user.id)
