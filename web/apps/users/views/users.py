from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer, UserUpdateForAdminLevelSerializer, UserUpdateForGeneralLevelSerializer
from users.permissions import IsAdminLevel
from users.constants import UserLevelEnum

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminLevel]
    lookup_field = "id"

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'post':
            pass
        # elif self.action == 'retrieve':
        #     return UserUpdateForGeneralLevelSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        return super(UserViewSet, self).get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.level == UserLevelEnum.ADMIN.value:
            self.serializer_class = UserUpdateForAdminLevelSerializer
        elif 'level' in request.data:
            return Response({"message": '등급 수정권한이 없습니다.'}, status.HTTP_401_UNAUTHORIZED)
        else:
            self.serializer_class = UserUpdateForGeneralLevelSerializer

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    