from django.shortcuts import render
from django.conf import settings
from django.views.decorators.http import require_http_methods
from client.libs.custom_decorators import login_required
from products.serializers import ProductSerializer
from client.pagination import ProductPagination
from client.permissions import IsLoggedInUser
from client.libs.cache import cache_get_product_count

from products.models import Product
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator

from django.shortcuts import redirect
import random
from drf_spectacular.utils import extend_schema
from products.constants import CategoryEnum

DEFAULT_CONFIG = {
    "websocket_host": settings.WEBSOCKET_HOST,
}

@extend_schema(
    exclude=True
)
@method_decorator(login_required, name="get")
class ProductTemplateViewSet(ListAPIView):
    queryset = Product.objects.filter(is_deleted="N")
    serializer_class = ProductSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'client/home.html'
    pagination_class = ProductPagination
    # permission_classes = [IsLoggedInUser, ]

    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.get_paginated_response(self.paginate_queryset(queryset))
        cate_dict = {
            "UNDEFINED": 1,
            "PANTS": 2,
            "TOPS": 3,
            "SHOES": 4,
        }

        # NOTE: 임시 예시
        count = cache_get_product_count(queryset, request.user.id)
        context = {
            'prod_list': page['results'],
            'page_links': page['links'],
            'page_count': page['num_pages'],
            'page_num': page['num'],
            'cate_dict': cate_dict,
            'is_logged_in': request.user.is_authenticated,
            'user': request.user,
            'rand_svg_num': random.randint(1287, 1336),
            'product_count': count,
            'default_config': DEFAULT_CONFIG,
        }
        return Response(context)
    
@require_http_methods(['GET'])
@login_required
def render_fitting(request):
    prod_list = list(Product.objects.filter(user_id=request.user.id, is_deleted="N", is_active="Y"))
    # TODO: Serializer data로 반환하기
    tops_prod_list = list(filter(lambda x: x.category == CategoryEnum.TOPS.value, prod_list))
    pants_prod_list = list(filter(lambda x: x.category == CategoryEnum.PANTS.value, prod_list))
    shoes_prod_list = list(filter(lambda x: x.category == CategoryEnum.SHOES.value, prod_list))

    data = [
        {
            "category": CategoryEnum.TOPS.value,
            "prod_list": tops_prod_list,
        }, {
            "category": CategoryEnum.PANTS.value,
            "prod_list": pants_prod_list,
        }, {
            "category": CategoryEnum.SHOES.value,
            "prod_list": shoes_prod_list,
        }
    ]
    context = {
        'data': data,
        'prod_list': prod_list,
        'is_logged_in': request.user.is_authenticated,
        'user': request.user,
        'rand_svg_num': random.randint(1287, 1336),
        'default_config': DEFAULT_CONFIG,
    }

    return render(request, 'client/fitting.html', context)

def e_handler401(request):
    return redirect("/accounts/login/")