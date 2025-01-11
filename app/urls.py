from django.urls import path
from app import views 
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('profile-detail/', views.ProfilDetailAPIView.as_view(), name='profile-detail'),

    path('users/update/', views.UserUpdateAPIView.as_view(), name='user-update'),
    path('users/register/', views.UserRegister.as_view(), name='user-register'),
    path('users/verify/', views.VerifyAPIView.as_view(), name='user-verify'),
    path('users/resend-code/', views.ResendCodeAPIView.as_view(), name='resend-code'),
    path('users/login/', views.LoginAPIView.as_view(), name='user-login'),
    path('users/get/', views.GetUserAPI.as_view(), name='get-user'),
    path('users/profile/', views.GetProfileAPI.as_view(), name='get-profile'),
    path('users/products/list', views.UserProductListView.as_view(), name='user-products'),

    path('verification-code/<int:user_id>/', views.CodeAPI.as_view(), name='get_verification_code'),

    path('products/list/', views.ProductListAPIView.as_view(), name='product-list'),
    path('products/information-detail/', views.ProductInformationAPIView.as_view(), name='product_information-detail'),
    path('products/create/', views.ProductCreateAPIView.as_view(), name='product-create'),
    path('products/comment-list/', views.CommentListAPIView.as_view(), name='product-comment-list'),
    path('products/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),
    path('products/category/', views.CategoryListView.as_view(), name='category-list'),

    path('private/information/create', views.CreatInformationView.as_view(), name='private_information-creat'),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]