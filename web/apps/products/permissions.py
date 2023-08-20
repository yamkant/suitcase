from rest_framework.permissions import BasePermission
from core.permissions import GenericAPIException
from users.constants import UserLevelEnum
from products.models import Product

SAFE_METHODS = ('GET', 'CREATE', 'HEAD', 'OPTIONS')

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user == obj.user_id:
                return True
            return False
        else:
            return False