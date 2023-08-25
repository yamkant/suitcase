from django.shortcuts import get_object_or_404, get_list_or_404

from functools import wraps
from core.permissions import GenericAPIException

import os
from django.shortcuts import redirect

import logging

logger = logging.getLogger("skeleton")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect('/accounts/login/')
        return func(request, *args, **kwargs)
    return wrapper