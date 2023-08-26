from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema_view
)
from products.serializers import ProductSerializer

PRODUCT_CREATE_EXAMPLES = [
    OpenApiExample(
        request_only=True,
        summary="[성공] 상품 등록 예시",
        description="""
            LEMARIE의 상의 상품을 등록하는 예시입니다.
            - response 403: 로그인을 하지 않은 상태에서 유저가 상품을 등록하려고 할 때 반환되는 값입니다.
        """,
        name="success_example",
        value={
            "name": "LEMAIRE TOP",
            "image_url": "https://us.lemaire.fr/cdn/shop/files/TO1105_LK121_BK858_PS1_1600x.jpg?v=1689067138",
            "category": 3,
        },
    ),
    OpenApiExample(
        request_only=True,
        summary="[실패] 요소 생략 예시",
        description="""
            이미지 url 없이 상품을 등록하는 예시입니다.
            - response 403: 로그인을 하지 않은 상태에서 유저가 상품을 등록하려고 할 때 반환되는 값입니다.
            - response 400: 요청 파라미터가 잘못 입력된 경우입니다.
        """,
        name="failure_example",
        value={
            "name": "Loro Piana BOTTOMS",
            "image_url": "",
            "category": 2,
        },
    ),
]