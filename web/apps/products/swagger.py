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
        description="""LEMARIE의 상의 상품을 등록하는 예시입니다.\n- response 403: 로그인을 하지 않은 상태에서 유저가 상품을 등록하려고 할 때 반환되는 값입니다.""",
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
        description="""이미지 url 없이 상품을 등록하는 예시입니다.\n- response 403: 로그인을 하지 않은 상태에서 유저가 상품을 등록하려고 할 때 반환되는 값입니다.\n- response 400: 요청 파라미터가 잘못 입력된 경우입니다.""",
        name="failure_example",
        value={
            "name": "Loro Piana BOTTOMS",
            "image_url": "",
            "category": 2,
        },
    ),
]

PRODUCT_LIST_EXAMPLES = [
    OpenApiParameter(
        name="page",
        type=int,
        required=False,
        description="페이지 번호를 입력하세요",
        examples=[
            OpenApiExample(
                name="page number",
                value=1,
            ),
        ]
    ),
    OpenApiParameter(
        name="page_size",
        type=int,
        required=False,
        description="페이지 크기를 입력하세요",
        examples=[
            OpenApiExample(
                name="page size",
                value=10,
            ),
        ]
    ),
    OpenApiParameter(
        name="search",
        type=str,
        required=False,
        description="검색어를 입력하세요",
        examples=[
            OpenApiExample(
                name="search",
                value='s',
            ),
        ]
    ),
]

PRODUCT_UPDATE_EXAMPLES = [
    OpenApiExample(
        request_only=True,
        summary="[성공] 상품 비활성화",
        description="""특정 상품을 비활성화 시킵니다. 비활성화된 상품은 Fitting 페이지에서 숨겨집니다.""",
        name="success_update__active",
        value={
            "is_active": "N",
        },
    ),
    OpenApiExample(
        request_only=True,
        summary="[성공] 상품 활성화",
        description="""특정 상품을 활성화 시킵니다. 활성화된 상품은 Fitting 페이지에서 볼 수 있습니다.""",
        name="success_update__deactive",
        value={
            "is_active": "Y",
        },
    ),
    OpenApiExample(
        request_only=True,
        summary="[성공] 상품명 수정 및 카테고리 수정",
        description="""'Edit product' modal에서 상품명과 상품의 카테고리를 수정합니다.""",
        name="success_update__product_info",
        value={
            "name": "수정된 상품",
            "category": 1,
        },
    ),
]