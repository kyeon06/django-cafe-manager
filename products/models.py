from django.db import models

class Product(models.Model):

    CATEGORY_CHOICES = [
        ('coffee', '커피'),
        ('non-coffee', '논커피'),
        ('beverage', '음료'),
        ('smoothie', '스무디'),
        ('ade', '에이드'),
        ('tea', '티'),
        ('dessert', '디저트'),
    ]

    SIZE_CHOICES = [
        ('S', 'Small'),
        ('L', 'Large'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES) # 카테고리
    price = models.IntegerField() # 가격
    cost = models.IntegerField() # 원가
    name = models.CharField(max_length=100) # 상품명
    description = models.TextField() # 상품설명
    barcode = models.CharField(max_length=50, unique=True) # 바코드
    expiration_date = models.DateField() # 유통기한
    size = models.CharField(max_length=1, choices=SIZE_CHOICES) # 사이즈
