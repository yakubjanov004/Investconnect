from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView,RetrieveUpdateAPIView
from app import serializers
from app import models
from .models import UserModel
from rest_framework.permissions import AllowAny
from django.db.utils import IntegrityError
from .serializers import Userserializer,VerifySerializer, LoginSerializer
from rest_framework.views import APIView,Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework import generics

class UserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = Userserializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')

        if UserModel.objects.filter(phone=phone, status='approwed').exists():
            raise serializers.ValidationError({"error": "Bunday telefon raqam bilan foydalanuvchi allaqachon mavjud."})

        try:
            user = UserModel.objects.create(phone=phone, username=username)
            user.set_password(password)
            user.generate_verification_code()  
            user.save()

            return Response(data={"user": user.id}, status=201)

        except IntegrityError:
            raise serializers.ValidationError({"error": "Bunday telefon raqam bilan foydalanuvchi allaqachon mavjud."})

class VerifyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        code = serializer.validated_data.get('code')

        if timezone.now() > user.expire_date or code != user.code:
            raise serializers.ValidationError({"error": "Kod eskirgan yoki noto‘g‘ri."})

        user.status = 'approwed'
        user.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response(data={"token": token.key, "user": user.id})

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "user": user.id})
from app import serializers, models




class UserModelListAPIView(ListAPIView):
    serializer_class = serializers.UserModelSerializer
    queryset = models.UserModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  

from django.contrib.auth.models import AnonymousUser
from app.models import Product, UserModel

class ProductListAPIView(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = models.Product.objects.all()
    filter_backends =  [DjangoFilterBackend,SearchFilter]
    filterset_fields = ('degree',)
    search_fields = ('name',)

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Product.objects.none()  
        try:
            user_instance = UserModel.objects.get(id=user.id)
            return Product.objects.filter(user=user_instance)
        except UserModel.DoesNotExist:
            return Product.objects.none()



class CommentListAPIView(ListAPIView):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        if product_id:
            return models.Comment.objects.filter(product_id=product_id)
        return models.Comment.objects.all()



class ProductCreateAPIView(CreateAPIView):
    serializer_class = serializers.CreateProductSerializer
    queryset = models.Product.objects.all()


class RegistrCreateAPIView(CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    queryset = models.UserModel.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    queryset = models.UserModel.objects.all()

    def get_object(self):
        return get_object_or_404(models.UserModel, id=self.request.user.id)


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()  # Barcha mahsulotlar
    serializer_class = serializers.ProductDetailSerializer  # Mahsulotlar uchun serializer
    lookup_field = 'id'

class ProfilDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = serializers.ProfilDetailSerializers
    queryset = models.UserModel.objects.all()