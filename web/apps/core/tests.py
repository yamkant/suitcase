from django.test import TestCase
from typing import Optional, Dict
from django.core.serializers.base import Serializer
from core.serializers import CreateSerializer, UpdateSerializer
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
        elif isinstance(self.serializer(), UpdateSerializer):
            return self.update(instance, data)

        if not instance:
            raise ValueError("instance must be a ModelSerializer")
        return self.serializer(instance)

    def create(self, data):
        serializer = self.serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            return serializer

    def update(self, instance, data):
        serializer = self.serializer(instance, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            updated_instance = serializer.save()
            return serializer

class ViewSetTestCase(TestCase):
    def generic_test(
        self,
        url,
        method,
        expected_status_code,
        client: Optional[APIClient] = None,
        **data,
    ):
        request = getattr(client, method)

        headers = {}
        response = request(
            url,
            data=data,
            format='json',
            **headers,
        )
        self.assertEqual(expected_status_code, response.status_code)
        return response