from django.urls import path
from .views import ProductAPIView, ProductSearchAPIView, ProductListAPIView
urlpatterns = [
    path("list/", ProductListAPIView.as_view()), # 싱픔 목록 조회
    path("", ProductAPIView.as_view()), # post - 상품 등록
    path("<int:pk>/", ProductAPIView.as_view()), # delete - 상품삭제, get - 상품상세정보, put - 상품정보수정
    path("search", ProductSearchAPIView.as_view()), # 검색 조회
]