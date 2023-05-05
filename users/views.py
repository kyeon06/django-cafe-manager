from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from cafe_manager.custom_response import CustomResponse

import jwt
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from cafe_manager.my_settings import SECRET_KEY

class RegisterAPIView(APIView):

    # 회원가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            data = {
                "user": serializer.data,
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            }
            res = CustomResponse(data=data, message="회원가입 완료", status=status.HTTP_200_OK)
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        
        return CustomResponse(data=serializer.errors, message="유효성검사 실패", status=status.HTTP_400_BAD_REQUEST)
    

class AuthAPIView(APIView):

    def get(self, request):
        try:
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return CustomResponse(data=serializer.data, status=status.HTTP_200_OK)
        
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰이 만료되었을 경우 토큰을 갱신한다.
            data = {
                'refresh' : request.COOKIES.get('refresh', None)
            }

            serializer = TokenRefreshSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])

                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = CustomResponse(data=serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cokkie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError
        
        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 경우
            return CustomResponse(message="토큰 사용이 불가능합니다.", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        # 유저 인증
        user = authenticate(
            phone_number = request.data.get('phone_number'),
            password = request.data.get('password')
        )

        # 1. 회원 가입한 유저일 경우
        if user is not None:
            serializer = UserSerializer(user)

            # jwt 토큰 접근해서 인증 요청
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            data = {
                "user" : serializer.data,
                "token" : {
                    "access" : access_token,
                    "refresh" : refresh_token,
                }

            }
            res = CustomResponse(data=data, message="로그인 성공", status=status.HTTP_200_OK)

            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return CustomResponse(message="해당 유저가 존재하지 않습니다. 회원가입 먼저 진행해주세요.",status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제(로그아웃)
        res = CustomResponse(message="로그아웃 완료", status=status.HTTP_202_ACCEPTED)
        res.delete_cookie("access")
        res.delete_cookie("refresh")
        return res