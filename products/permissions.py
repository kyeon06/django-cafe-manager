from rest_framework import permissions

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    로그인한 유저만 상품 관련 API에 접근 가능하도록 권한을 제한
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
