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
    path('products/information-detail/<int:product_id>', views.PrivateProductDetailsView.as_view(), name='product_information-detail'),
    path('products/create/', views.ProductCreateAPIView.as_view(), name='product-create'),
    path('products/comment-list/', views.CommentListAPIView.as_view(), name='product-comment-list'),
    path('products/<int:id>/', views.PublicProductsView.as_view(), name='product-detail'),
    path('products/category/', views.CategoryListView.as_view(), name='category-list'),


    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('payment-and-check/', views.PaymentAndCheckView.as_view(), name='payment-and-check'),

    path('investor-products/', views.UserPurchasedProductsView.as_view(), name='investor-products'),
    ##############################################################################################

    path('create-product_1/', views.ProductCreateView.as_view(), name='create-product'),

    path('api/public-products/', views.PublicProductAPIView.as_view(), name='public-products'),
    path('api/private-products/', views.PrivateProductAPIView.as_view(), name='private-products'),

    # path('api/unlock-product/<int:product_id>/', views.UnlockPrivateProductAPIView.as_view(), name='unlock-product'),
    
    path('api/payment-unlock/', views.PaymentAndUnlockView.as_view(), name='payment-unlock'),

]