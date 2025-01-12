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
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound


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
      user_data = []
      for user in users:
        profile_image_url = user.profile_image.url if user.profile_image else None
        user_data.append({
          "id": user.id,
          "firstname": user.firstname,
          "lastname": user.lastname,
          "profile_image": profile_image_url,
          "phone": user.phone,
          "email": user.email,
          "role": user.role,
        })
      return Response(user_data, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class GetProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            user_data = {
                "id": user.id,
                "username": user.username,
                "profile_image": user.profile_image.url if user.profile_image else None,
                "phone": getattr(user, 'phone', None),
                "role": getattr(user, 'role', None),
            }
            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class VerifyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        code = serializer.validated_data.get('code')

        if timezone.now() > user.expire_date:
            user.delete()  
            raise ValidationError({"error": "Kod muddati tugagan, foydalanuvchi o‘chirildi."})
        if code != user.code:
            raise ValidationError({"error": "Kod noto‘g‘ri."})
        user.status = UserModel.UserAuthStatus.APPROVED
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={"token": token.key, "user": user.id})
    


class ResendCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')  
        if not phone:
            raise ValidationError({"error": "Telefon raqamni kiriting."})        
        try:
            user = UserModel.objects.get(phone=phone, status=UserModel.UserAuthStatus.NEW)
        except UserModel.DoesNotExist:
            raise ValidationError({"error": "Telefon raqam topilmadi yoki foydalanuvchi allaqachon tasdiqlangan."})
        if user.expire_date is None or user.expire_date < timezone.now():
            print("asa")
            user.generate_verification_code()
            user.save()

        return Response(
            {"code": user.code}, 
            status=status.HTTP_200_OK
        )



class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            user = authenticate(request=request, username=phone, password=password)           
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class UserModelListAPIView(ListAPIView):
    serializer_class = serializers.UserModelSerializer
    queryset = models.UserModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  



class ProductListAPIView(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = models.Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ('category__name',)
    search_fields = ('name',)



class ProductInformationAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.ProductinformationSerializer
    queryset = models.PrivateInformation.objects.all()
    lookup_field = 'id'



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

    def create(self, request, *args, **kwargs):
        product_images = request.FILES.getlist('product_images') 
        data = request.data.copy() 
        data['product_images'] = product_images  

        if len(product_images) > 8:
            raise ValidationError({"error": "Siz bir vaqtning o'zida 8 tadan ortiq rasm yuborishingiz mumkin emas."})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        product = serializer.save()

        for image in product_images:
            ProductImage.objects.create(product=product, image=image)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UserUpdateAPIView(UpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(models.UserModel, id=self.request.user.id)



class ProductDetail(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()  
    serializer_class = serializers.ProductDetailSerializer  
    lookup_field = 'id'



class ProfilDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = serializers.ProfilDetailSerializers
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(models.UserModel, id=self.request.user.id)



class CategoryListView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer



class CreatInformationView(generics.CreateAPIView):
    queryset = models.PrivateInformation.objects.all()
    serializer_class = serializers.InformationSerializer



class UserProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_products = models.Product.objects.filter(user=request.user)
        serializer = serializers.UserProductSerializer(user_products, many=True)
        return Response(serializer.data)
    
class PublicProductsView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            product = models.Product.objects.get(id=id)
            data = {
                "name": product.name,
                "description": product.description,
                "location": product.location,
                "image": product.image.url if product.image else None,
                "price": product.price,
                "category": product.category.name if product.category else None,
            }
            return Response(data)
        
        except models.Product.DoesNotExist:
            raise NotFound(detail="Product not found")



class PrivateProductDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id, *args, **kwargs):
        payment = models.Payment.objects.filter(
            investor=request.user,
            product_id=product_id,
            is_active=True
        ).exists()

        if not payment:
            return Response({"error": "To'lov qilinmagan"}, status=403)

        try:
            private_info = models.PrivateInformation.objects.get(product_id=product_id)
        except models.PrivateInformation.DoesNotExist:
            return Response({"error": "Maxsus ma'lumot topilmadi"}, status=404)

        data = {
            "status": private_info.status,
            "kampanya_egasi": private_info.kampanya_egasi,
            "kontact": private_info.kontact,
            "campany_name": private_info.campany_name,
            "oylik_daromadi": private_info.oylik_daromadi,
            "soff_foydasi": private_info.soff_foydasi,
        }
        return Response({"private_info": data})







class PaymentAndCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        amount = request.data.get('amount')

        if amount != 10:
            return Response({"error": "To'lov miqdori 10$ bo'lishi kerak"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = models.Product.objects.get(id=product_id)
        except models.Product.DoesNotExist:
            return Response({"error": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        # Foydalanuvchi to'lovni tekshiradi
        payment = models.Payment.objects.filter(investor=request.user, product=product, is_active=True).first()

        if payment:
            try:
                private_info = models.PrivateInformation.objects.get(product=product)
            except models.PrivateInformation.DoesNotExist:
                return Response({"error": "Maxsus ma'lumot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

            data = {
                "status": private_info.status,
                "kampanya_egasi": private_info.kampanya_egasi,
                "kontact": private_info.kontact,
                "campany_name": private_info.campany_name,
                "oylik_daromadi": private_info.oylik_daromadi,
                "soff_foydasi": private_info.soff_foydasi,
            }
            return Response({"private_info": data, "message": "To'lov mavjud"})

        else:
            payment = models.Payment.objects.create(
                investor=request.user,
                product=product,
                amount=amount,
                is_active=True
            )
            return Response({"message": "To'lov muvaffaqiyatli amalga oshirildi", "payment_id": payment.id})

class UserPurchasedProductsView(ListAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Product.objects.filter(
            payment__investor=self.request.user,  # Foydalanuvchi to'lovlari
            payment__is_active=True  # Faqat faol to'lovlar
        ).distinct()
