from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsAdminLevelOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminLevelOrReadOnly]

    # def get_permissions(self):
    #     permission_classes = [AdminLevelPermission, ]

    #     return permission_classes


    def get_queryset(self):
        return User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'post':
            pass
        return super().get_serializer_class()