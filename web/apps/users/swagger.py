from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema_view
)
from users.constants import UserLevelEnum

USER_UPDATE_EXAMPLES = [
    OpenApiExample(
        request_only=True,
        summary="[성공] 사용자 연동 url 수정",
        description="""일반 유저의 경우, 연동 url을 수정할 수 있습니다.""",
        name="success_example",
        value={
            "user_url": "test@example.com",
        },
    ),
    OpenApiExample(
        request_only=True,
        summary="[실패] 사용자 level 수정",
        description="""관리자 권한을 받지 않은 유저는 다른 유저의 등급을 수정할 수 없습니다.""",
        name="failure_example",
        value={
            "level": UserLevelEnum.ADMIN.value,
        },
    ),
]