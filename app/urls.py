from django.urls import path
from app import views 

urlpatterns = [
    path('profile-detail/<int:pk>/', views.ProfilDetailAPIView.as_view(), name='profil'),

    path('users/update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user-update'),
    path('users/register/', views.UserRegister.as_view(), name='user-register'),
    path('users/verify/', views.VerifyAPIView.as_view(), name='user-verify'),
    path('users/login/', views.LoginAPIView.as_view(), name='user-login'),
    path('verification-code/<int:user_id>/', views.CodeAPI.as_view(), name='get_verification_code'),
    path('users/get/', views.GetUserAPI.as_view(), name='get-user'),

    path('products/list/', views.ProductListAPIView.as_view(), name='product-list'),
    path('products/listyana/', views.ProductyanaListAPIView.as_view(), name='product-list'),
    path('products/create/', views.ProductCreateAPIView.as_view(), name='product-create'),
    path('products/comment-list/', views.CommentListAPIView.as_view(), name='product-comment-list'),
    path('products/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),
]