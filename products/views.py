from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import CursorPagination
from rest_framework import status
from .serializers import ProductSerializer
from cafe_manager.custom_response import CustomResponse
from .models import Product

# Pagination
class ProductCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'category'
    cursor_query_param = 'cursor'

# 상품 목록 조회
class ProductListAPIView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    pagination_class = ProductCursorPagination
    queryset = Product.objects.all()

    def get(self, request, **kwags):
        queryset = Product.objects.all()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse(data=serializer.data, status=status.HTTP_200_OK)

# 상품 상세
class ProductAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer

    # 상품 조회
    def get(self, request, **kwags):
        if kwags.get('pk') is None:
            return CustomResponse(message="잘못된 요청입니다.", status=status.HTTP_400_BAD_REQUEST)
        else:

            try:    
                product_id = kwags.get('pk')
                product_object = Product.objects.get(id=product_id)
                serializer = self.serializer_class(product_object)
                return CustomResponse(data=serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return CustomResponse(message="상품 정보가 존재하지 않습니다.",status=status.HTTP_404_NOT_FOUND)

    # 상품 등록
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

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
            
            serializer = self.serializer_class(product_object, data=request.data, partial=True)
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
            
# 상품 검색 조회
class ProductSearchAPIView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    pagination_class = ProductCursorPagination
    queryset = Product.objects.all()


    # 상품 검색
    def get(self, request):
        keyword = self.request.GET.get('keyword', '')

        if keyword:
            queryset = Product.objects.filter(name__contains=keyword)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.serializer_class(queryset, many=True)
            
            return CustomResponse(data=serializer.data, message="검색 성공", status=status.HTTP_200_OK)
        else:
            return CustomResponse(data=None, message="검색 키워드를 입력해주세요", status=status.HTTP_400_BAD_REQUEST)