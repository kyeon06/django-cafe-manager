from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import CursorPagination
from rest_framework import status
from .serializers import ProductSerializer
from cafe_manager.custom_response import CustomResponse
from rest_framework.response import Response
from .models import Product


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