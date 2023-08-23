from django.test import TestCase, override_settings
from typing import Optional, Dict
from django.core.serializers.base import Serializer
from core.serializers import CreateSerializer, UpdateSerializer
from django.core.serializers.base import Serializer
from rest_framework.serializers import ModelSerializer
from rest_framework.test import APIClient

# common
from django.test import TestCase

import logging
logger = logging.getLogger("skeleton")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

from django.db import connection, reset_queries
def assert_query_count(count):
    def decorator(func):
        @override_settings(DEBUG=True)
        def wrapper(*args, **kwargs):
            reset_queries()
            ret = func(*args, **kwargs)
            queries = connection.queries
            for query in queries:
                logger.debug(f"QUERY: {query['sql']}, TIME: {query['time']}")
            assert len(queries) == count, "QUERY COUNT:%d != %d" % (len(queries), count)
            return ret
        return wrapper
    return decorator

class IntegrationSerializerTestCase(TestCase):
    def serializer_test(
        self,
        expected_query_count: int = None,
        instance: Optional[ModelSerializer] = None,
        **data,
    ):
        run_test = self.run_test
        if expected_query_count:
            run_test = assert_query_count(expected_query_count)(run_test)
        return run_test(instance, data)

    def run_test(self, instance, data):
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
        serializer = self.serializer(instance, data=data, partial=False)
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