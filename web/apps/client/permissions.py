
from rest_framework.permissions import BasePermission
from django.template import RequestContext

from rest_framework import permissions
from core.permissions import GenericAPIException

class IsLoggedInUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise GenericAPIException(status_code=401)
        return request.user.is_authenticated 