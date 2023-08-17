from rest_framework.permissions import BasePermission
from core.permissions import GenericAPIException
from users.constants import UserLevelEnum

SAFE_METHODS = ('GET', 'PATCH', 'HEAD', 'OPTIONS')

class IsAdminLevel(BasePermission):
    def is_valid_level(self, level):
        return (
            level == UserLevelEnum.ADMIN.value
        )

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not self.is_valid_level(request.user.level):
            raise GenericAPIException(status_code=401)
        
        return request.user.is_authenticated 