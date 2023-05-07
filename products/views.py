from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import CursorPagination
from rest_framework import status
from .serializers import ProductSerializer
from cafe_manager.custom_response import CustomResponse
from rest_framework.response import Response
from .models import Product

from urllib import parse


class ProductAPIView(APIView):

    # 상품 조회
    def get(self, request, **kwags):

        if kwags.get('pk') is None:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
            return CustomResponse(data=serializer.data, status=status.HTTP_200_OK)
        else:

            try:    
                product_id = kwags.get('pk')
                product_object = Product.objects.get(id=product_id)
                serializer = ProductSerializer(product_object)
                return CustomResponse(data=serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return CustomResponse(message="상품 정보가 존재하지 않습니다.",status=status.HTTP_404_NOT_FOUND)

    # 상품 등록
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return CustomResponse(data=serializer.data, message="상품이 등록되었습니다." ,status=status.HTTP_201_CREATED)
       
        return CustomResponse(data=serializer.errors, message="상품 정보를 다시 확인해주세요." ,status=status.HTTP_400_BAD_REQUEST)
    
    # 상품 수정
    def put(self, request, **kwags):
        if kwags.get('pk') is None:
            return CustomResponse(data=None, message="잘못된 요청입니다.", status=status.HTTP_400_BAD_REQUEST)
        else:

            try:
                product_id = kwags.get('pk')
                product_object = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return CustomResponse(message="상품 정보가 존재하지 않습니다.",status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProductSerializer(product_object, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(data=serializer.data, status=status.HTTP_200_OK)
            return CustomResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # 상품 삭제
    def delete(self, request, **kwags):
        if kwags.get('pk') is None:
            return CustomResponse(data=None, message="잘못된 요청입니다.", status=status.HTTP_400_BAD_REQUEST)
        else:

            try:
                product_id = kwags.get('pk')
                product_object = Product.objects.get(id=product_id)
                product_object.delete()
                return CustomResponse(message="삭제가 완료되었습니다.", status=status.HTTP_200_OK)
            
            except Product.DoesNotExist:
                return CustomResponse(message="상품 정보가 존재하지 않습니다.",status=status.HTTP_404_NOT_FOUND)
            
from hangul_utils import split_syllables, join_jamos
from django.db.models import Q

class ProductSearchAPIView(ListAPIView):
    serializer_class = ProductSerializer

    # 상품 검색
    def get(self, request):
        keyword = self.request.GET.get('keyword', '')

        if keyword:
            queryset = Product.objects.filter(name__contains=keyword)
            
            serializer = self.serializer_class(queryset, many=True)
            return CustomResponse(data=serializer.data, message="검색 성공", status=status.HTTP_200_OK)
        else:
            return CustomResponse(data=None, message="검색 키워드를 입력해주세요", status=status.HTTP_400_BAD_REQUEST)