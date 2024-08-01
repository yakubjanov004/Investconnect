from django.urls import path
from app import views 

urlpatterns = [
    path('usermodel-list/', views.UserModelListAPIView.as_view()),
    path('product-list/', views.ProductListAPIView.as_view()),
    path('comment-list/', views.ProductListAPIView.as_view()),

]
