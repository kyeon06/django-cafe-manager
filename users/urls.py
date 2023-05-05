from django.contrib import admin
from django.urls import path
from .views import RegisterAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()), # post - 회원가입
]