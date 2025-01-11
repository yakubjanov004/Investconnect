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
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = Userserializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')
        role = serializer.validated_data.get('role')

        if UserModel.objects.filter(username=username, status='approwed').exists():
            raise ValidationError({"error": "Bunday username bilan foydalanuvchi allaqachon mavjud."})

        if UserModel.objects.filter(phone=phone, status='approwed').exists():
            raise ValidationError({"error": "Bunday telefon raqam bilan foydalanuvchi allaqachon mavjud."})

        try:
            user = UserModel.objects.create(username=username, phone=phone, role=role)
            user.set_password(password)
            user.generate_verification_code()
            user.save()

            return Response(data={"user": user.id}, status=201)

        except IntegrityError as e:
            if "username" in str(e):
                raise ValidationError({"error": "Bunday username bilan foydalanuvchi allaqachon mavjud."})
            elif "phone" in str(e):
                raise ValidationError({"error": "Bunday telefon raqam bilan foydalanuvchi allaqachon mavjud."})
            else:
                raise ValidationError({"error": "Foydalanuvchini yaratishda xato yuz berdi."})


            
class CodeAPI(APIView):

    def get(self, request, user_id):
        user = get_object_or_404(UserModel, id=user_id)

        if user.code:
            return Response({
                "id": user.id,
                "verification_code": user.code,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "Verifikatsiya kodi topilmadi."
            }, status=status.HTTP_404_NOT_FOUND)
        
class GetUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            users = UserModel.objects.all() 
            user_data = [
                {
                    "id": user.id,  
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "phone": user.phone,
                    "email": user.email,
                    "role": user.role,
                }
                for user in users
            ]
            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = UserModel.objects.get(id=user_id)  
            user_data = {
                "id": user.id,
                "username": user.username,               
                "phone": user.phone,
                "role": user.role,
            }
            return Response(user_data, status=status.HTTP_200_OK)
        except UserModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



#class VerifyAPIView(APIView):
    # permission_classes = [AllowAny]

    # def post(self, request, *args, **kwargs):
    #     serializer = VerifySerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     user = serializer.validated_data.get('user')
    #     code = serializer.validated_data.get('code')

    #     if timezone.now() > user.expire_date:
    #         user.delete()  
    #         raise ValidationError({"error": "Kod muddati tugagan, foydalanuvchi o‘chirildi."})

    #     if code != user.code:
    #         raise ValidationError({"error": "Kod noto‘g‘ri."})

    #     user.status = 'approwed'
    #     user.save()
    #     token, _ = Token.objects.get_or_create(user=user)

    #     return Response(data={"token": token.key, "user": user.id})
class VerifyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Serializerni yaratish
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validatsiyani bajarish
        print(f"Serializer validatsiya qilingan: {serializer.validated_data}")  # Validatsiya natijasi

        # Foydalanuvchi va kodni olish
        user = serializer.validated_data.get('user')
        code = serializer.validated_data.get('code')
        print(f"Foydalanuvchi: {user}, Kod: {code}")  # Foydalanuvchi va kodni tekshirish

        # Kod muddati tugaganini tekshirish
        if timezone.now() > user.expire_date:
            print(f"Foydalanuvchi {user.id} ning kodi muddati tugagan.")  # Kod muddati tugagan
            user.delete()  # Foydalanuvchi o'chiriladi
            raise ValidationError({"error": "Kod muddati tugagan, foydalanuvchi o‘chirildi."})

        # Kod noto'g'ri ekanligini tekshirish
        if code != user.code:
            print(f"Foydalanuvchi {user.id} ning kodi noto‘g‘ri.")  # Kod noto'g'ri bo'lsa
            raise ValidationError({"error": "Kod noto‘g‘ri."})

        # Foydalanuvchini tasdiqlash
        user.status = 'approwed'
        user.save()  # Foydalanuvchi statusini o'zgartirish
        print(f"Foydalanuvchi {user.id} tasdiqlandi va saqlandi.")  # Foydalanuvchi tasdiqlangan

        # Token yaratish
        token, _ = Token.objects.get_or_create(user=user)
        print(f"Token yaratildi: {token.key}")  # Yaratilgan token

        # Javob qaytarish
        return Response(data={"token": token.key, "user": user.id})


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "user": user.id})
    
class UserModelListAPIView(ListAPIView):
    serializer_class = serializers.UserModelSerializer
    queryset = models.UserModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  



class ProductListAPIView(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = models.Product.objects.all()
    filter_backends =  [DjangoFilterBackend,SearchFilter]
    filterset_fields = ('degree','category__name')
    search_fields = ('name',)

class ProductInformationListAPIView(ListAPIView):
    serializer_class = serializers.ProductinformationListSerializer
    queryset = models.Information.objects.all()
    filter_backends =  [DjangoFilterBackend,SearchFilter]
    filterset_fields = ('key','value')
    search_fields = ('key',)


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
    queryset = models.Product.objects.all()  
    serializer_class = serializers.ProductDetailSerializer  
    lookup_field = 'id'

class ProfilDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = serializers.ProfilDetailSerializers
    queryset = models.UserModel.objects.all()


class CategoryListView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class CreatInformationView(generics.CreateAPIView):
    queryset = models.Information.objects.all()
    serializer_class = serializers.InformationSerializer