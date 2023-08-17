from rest_framework import serializers
from core.serializers import CreateSerializer

from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone",
            "level",
        )
        read_only_fields = fields

class UserCreateSerializer(CreateSerializer):
    representation_serializer_class = UserSerializer
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "password",
            "password2",
        )
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "비밀번호가 다릅니다."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)