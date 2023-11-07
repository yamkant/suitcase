from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ValidationError,
)
from apps.core.serializers import ReperesntationSerializerMixin

from apps.users.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "level",
            "user_url",
        )
        read_only_fields = fields

class UserCreateSerializer(ReperesntationSerializerMixin, ModelSerializer):
    representation_serializer_class: UserSerializer = UserSerializer
    password2 = CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
        )
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError({"password2": "비밀번호가 다릅니다."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

# NOTE: Full Account / Basic Account인지 
class UserUpdateForGeneralLevelSerializer(ReperesntationSerializerMixin, ModelSerializer):
    representation_serializer_class: UserSerializer = UserSerializer

    class Meta:
        model = User
        fields = (
            "user_url",
        )
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class UserUpdateForAdminLevelSerializer(ReperesntationSerializerMixin, ModelSerializer):
    representation_serializer_class: UserSerializer = UserSerializer

    class Meta:
        model = User
        fields = (
            "level",
        )
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)