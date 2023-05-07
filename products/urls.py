from django.urls import path
from .views import ProductAPIView
urlpatterns = [
    path("", ProductAPIView.as_view()), # get, post
    path("<int:pk>/", ProductAPIView.as_view()), # delete - 상품삭제, get - 상품상세정보, put - 상품정보수정
]