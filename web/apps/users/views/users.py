from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    # def get_permissions(self):
    #     pass
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'post':
            pass
        return super().get_serializer_class()