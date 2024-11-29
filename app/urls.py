from django.urls import path
from app import views 

urlpatterns = [
    path('product-list/', views.ProductListAPIView.as_view()),
    path('comment-list/', views.ProductListAPIView.as_view()),
    path('creat-prduct/', views.ProductCreateAPIView.as_view()),
    path('user-update/<int:pk>/', views.UserUpdateAPIView.as_view()),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('verify/', views.VerifyAPIView.as_view(), name='verify'),
    path('login/', views.LoginAPIView.as_view(), name='login')

]
