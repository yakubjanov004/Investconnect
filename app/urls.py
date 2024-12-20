from django.urls import path
from app import views 

urlpatterns = [
    path('profile-detail/<int:pk>/', views.ProfilDetailAPIView.as_view(), name='profil'),

    path('users/update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user-update'),
    path('users/register/', views.UserRegister.as_view(), name='user-register'),
    path('users/verify/', views.VerifyAPIView.as_view(), name='user-verify'),
    path('users/login/', views.LoginAPIView.as_view(), name='user-login'),
    path('users/get/', views.GetUserAPI.as_view(), name='get-user'),
    path('users/profile-get/<int:user_id>/', views.GetProfileAPI.as_view(), name='get-profile-user'),

    path('verification-code/<int:user_id>/', views.CodeAPI.as_view(), name='get_verification_code'),

    path('products/list/', views.ProductListAPIView.as_view(), name='product-list'),
    path('products/information-list/', views.ProductInformationListAPIView.as_view(), name='product-list'),
    path('products/create/', views.ProductCreateAPIView.as_view(), name='product-create'),
    path('products/comment-list/', views.CommentListAPIView.as_view(), name='product-comment-list'),
    path('products/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),
    path('products/category/', views.CategoryListView.as_view(), name='category-list'),

    path('Information/create', views.CreatInformationView.as_view(), name='information-creat'),
]