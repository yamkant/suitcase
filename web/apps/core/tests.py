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
