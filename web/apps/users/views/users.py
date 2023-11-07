from rest_framework.viewsets import (
    ModelViewSet,
)
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import JSONParser

from apps.users.models import User
from apps.users.serializers import UserSerializer, UserUpdateForAdminLevelSerializer, UserUpdateForGeneralLevelSerializer
from apps.users.permissions import IsAdminLevel
from apps.users.constants import UserLevelEnum
from apps.users.swagger import USER_UPDATE_EXAMPLES

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminLevel]
    parser_classes = [JSONParser]
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
    
    @extend_schema(
        request=UserSerializer,
        summary="유저 목록을 조회합니다.",
        description="""전체 유저 목록을 조회합니다. (이후, 커뮤니티 관련기능 추가)""",
        tags=['유저'],
        responses={
            status.HTTP_200_OK: UserSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    @extend_schema(
        request=UserSerializer,
        summary="유저 정보를 업데이트합니다.",
        description="""유저의 등급에 따라 수정항목을 제한합니다.<br>- 관리자: 유저 등급 수정<br>- 일반: 유저 정보 수정""",
        tags=['유저'],
        examples=USER_UPDATE_EXAMPLES,
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_401_UNAUTHORIZED: None,
        }
    )
    def update(self, request, *args, **kwargs):
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
    