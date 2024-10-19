from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView
from app import serializers
from app import models
from .models import UserModel
from rest_framework.permissions import AllowAny
from django.db.utils import IntegrityError
from .serializers import Userserializer,VerifySerializer, LoginSerializer
from rest_framework.views import APIView,Response
from rest_framework.authtoken.models import Token
from django.utils import timezone

class UserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = Userserializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')

        if UserModel.objects.filter(phone=phone, status='approwed').exists():
            raise serializers.ValidationError({"error": "Bunday telefon raqam bilan foydalanuvchi allaqachon mavjud."})

        try:
            user = UserModel.objects.create(phone=phone)
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

class ProductListAPIView(ListAPIView):
    serializer_class = serializers.ProductListSerializers
    queryset = models.Product.objects.all()

class CommentListAPIView(ListAPIView):
    serializer_class = serializers.CommentSerializers
    queryset = models.Comment.objects.all()

class ProductCreateAPIView(CreateAPIView):
    serializer_class = serializers.CreatProductSerializers
    queryset = models.Product.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    queryset = models.UserModel.objects.all()
