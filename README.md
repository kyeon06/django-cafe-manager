# django-cafe-manager

## ✨ 구현 내용
---
### **1. 상품 등록**
- url path : `/product/`
- 요청방식 : `POST`
- request example
```
{
    "category": "coffee",
    "price": 3500,
    "cost": 3500,
    "name": "콜드브루",
    "description": "콜드브루",
    "barcode": "7436852619316",
    "expiration_date": "2030-12-31",
    "size": "L"
}
```
- response example
```
{
    "meta": {
        "code": 201,
        "message": "상품이 등록되었습니다."
    },
    "data": {
        "id": 15,
        "category": "coffee",
        "price": 3500,
        "cost": 3500,
        "name": "콜드브루",
        "description": "콜드브루",
        "barcode": "7436852619316",
        "expiration_date": "2030-12-31",
        "size": "L"
    }
}
```
<br>

### **2. 상품 목록 조회**
- url path : `/product/list/`
- 요청방식 : `GET`
- response example
```
{
    "next": "http://127.0.0.1:8000/product/list/?cursor=abc123",
    "previous": null,
    "results": [
        {
            "id": 12,
            "category": "beverage",
            "price": 3000,
            "cost": 3000,
            "name": "자몽허니블랙티",
            "description": "자몽허니블랙티",
            "barcode": "7436852619309",
            "expiration_date": "2030-12-31",
            "size": "L"
        },
        {
            "id": 3,
            "category": "coffee",
            "price": 1500,
            "cost": 1500,
            "name": "아메리카노",
            "description": "아메리카노",
            "barcode": "7436852619300",
            "expiration_date": "2030-12-31",
            "size": "L"
        }
    ]
}
```
<br>

### **3. 상품 상세 조회**
- url path : `/product/{pk}/`
- 요청방식 : `GET`
- response example
```
{
    "meta": {
        "code": 200,
        "message": "ok"
    },
    "data": {
        "id": 12,
        "category": "beverage",
        "price": 3000,
        "cost": 3000,
        "name": "자몽허니블랙티",
        "description": "자몽허니블랙티",
        "barcode": "7436852619309",
        "expiration_date": "2030-12-31",
        "size": "L"
    }
}
```
<br>

### **4. 상품 수정**
- url path : `/product/{pk}/`
- 요청방식 : `PUT`
- request example : 부분 수정 가능
```
{
    "size": "S"
}
```
- response example
```
{
    "meta": {
        "code": 200,
        "message": "ok"
    },
    "data": {
        "id": 3,
        "category": "coffee",
        "price": 1500,
        "cost": 1500,
        "name": "아메리카노",
        "description": "아메리카노",
        "barcode": "7436852619300",
        "expiration_date": "2030-12-31",
        "size": "S"
    }
}
```
<br>


### **5. 상품 삭제**
- url path : `/product/{pk}/`
- 요청방식 : `DELETE`
- respone example
```
{
    "meta": {
        "code": 200,
        "message": "삭제가 완료되었습니다."
    },
    "data": null
}
```

<br>

### **6. 상품 검색 기능**
- url path : `/product/search?keyword=라떼`
- 요청방식 : `GET`
- response example
```
{
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 6,
            "category": "non-coffee",
            "price": 3300,
            "cost": 3300,
            "name": "곡물라떼",
            "description": "곡물라떼",
            "barcode": "7436852619303",
            "expiration_date": "2030-12-31",
            "size": "L"
        },
        {
            "id": 7,
            "category": "non-coffee",
            "price": 3500,
            "cost": 3500,
            "name": "더블초코라떼",
            "description": "더블초코라떼",
            "barcode": "7436852619304",
            "expiration_date": "2030-12-31",
            "size": "L"
        }
    ]
}
```
<br>

### **7. 회원 가입**
- url path : `/user/register/`
- 요청방식 : `POST`
- request example
```
{
    "phone_number" : "010-2222-3333",
    "password" : "@Testuser3"
}
```
- response example
```
{
    "meta": {
        "code": 200,
        "message": "회원가입 완료"
    },
    "data": {
        "user": {
            "id": 9,
            "password": "",
            "last_login": null,
            "phone_number": "010-2222-3333",
            "is_active": true,
            "is_admin": false
        },
        "token": {
            "access": "",
            "refresh": ""
        }
    }
}
```
<br>

### **8. 로그인**
- url path : `/user/auth/`
- 요청방식 : `POST`
- response example
```
{
    "meta": {
        "code": 200,
        "message": "로그인 성공"
    },
    "data": {
        "user": {
            "id": 9,
            "password": "",
            "last_login": null,
            "phone_number": "010-2222-3333",
            "is_active": true,
            "is_admin": false
        },
        "token": {
            "access": "",
            "refresh": ""
        }
    }
}
```
<br>

### **9. 로그아웃**
- url path : `/user/auth/`
- 요청방식 : `DELETE`
- response example
```
{
    "meta": {
        "code": 202,
        "message": "로그아웃 완료"
    },
    "data": null
}
```
