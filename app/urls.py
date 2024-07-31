from django.urls import path
from app import views 

urlpatterns = [
    path('usermodel-list/', views.UserModelListAPIView.as_view()),

]
