from django.test import TestCase
from typing import Optional, Dict
from django.core.serializers.base import Serializer
from core.serializers import CreateSerializer
from django.core.serializers.base import Serializer
from rest_framework.serializers import ModelSerializer
from rest_framework.test import APIClient

# common
from django.test import TestCase

class IntegrationSerializerTestCase(TestCase):
    def serializer_test(
        self,
        instance: Optional[ModelSerializer] = None,
        **data,
    ):
        if isinstance(self.serializer(), CreateSerializer):
            return self.create(data)

        if not instance:
            raise ValueError("instance must be a ModelSerializer")
        return self.serializer(instance)

    def create(self, data):
        serializer = self.serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.create(data)
            return serializer
