from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView,RetrieveAPIView,RetrieveUpdateAPIView
from app import serializers
from app import models
from rest_framework.views import APIView,Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class UserModelListAPIView(ListAPIView):
    serializer_class = serializers.UserModelSerializers
    queryset = models.UserModel.objects.all()

class ProductListAPIView(ListAPIView):
    serializer_class = serializers.ProductListSerializers
    queryset = models.Product.objects.all()

class CommentListAPIView(ListAPIView):
    serializer_class = serializers.CommentSerializers
    queryset = models.Comment.objects.all()

class ProductCreateAPIView(CreateAPIView):
    serializer_class = serializers.CreatProductSerializers
    queryset = models.Product.objects.all()

class RegistrCreateAPIView(CreateAPIView):
    serializer_class = serializers.RegistrSerializers
    queryset = models.UserModel.objects.all()

class UserUpdateAPIView(UpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    queryset = models.UserModel.objects.all()
