from rest_framework.exceptions import APIException
from rest_framework import status

class GenericAPIException(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'error'

    def _get_error_message_by_status_code(self, status_code):
        if status_code == status.HTTP_401_UNAUTHORIZED:
            return "인증된 사용자만 접근 가능합니다."

    def __init__(self, detail=None, status_code=None):
        if detail is None:
            self.detail = self._get_error_message_by_status_code(status_code)
        else:
            self.detail = detail
        if status_code is not None:
            self.status_code = status_code