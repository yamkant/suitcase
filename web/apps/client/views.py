from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from client.libs.custom_decorators import login_required
from products.serializers import ProductSerializer
from client.pagination import ProductPagination
from client.permissions import IsLoggedInUser

from products.models import Product
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator

from django.shortcuts import redirect

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
        if request.user.is_anonymous:
            return redirect("/accounts/login/")
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.get_paginated_response(self.paginate_queryset(queryset))
        cate_dict = {
            "UNDEFINED": 1,
            "PANTS": 2,
            "TOPS": 3,
            "SHOES": 4,
        }

        context = {
            'prod_list': page['results'],
            'page_links': page['links'],
            'page_count': page['num_pages'],
            'page_num': page['num'],
            'cate_dict': cate_dict,
            'is_logged_in': request.user.is_authenticated,
            'username': request.user.username,
            'email': request.user.email,
        }
        return Response(context)
    
@require_http_methods(['GET'])
@login_required
def render_fitting(request):
    prod_list = Product.objects.filter(user_id=request.user.id, is_deleted="N", is_active="Y")
    # TODO: Enum to dictionary로 리팩토링
    cate_dict = {
        "UNDEFINED": 1,
        "PANTS": 2,
        "TOPS": 3,
        "SHOES": 4,
    }

    cate_disp_dict = {
        "TOPS": 3,
        "PANTS": 2,
        "SHOES": 4,
    }

    context = {
        'prod_list': prod_list,
        'cate_dict': cate_dict,
        'cate_disp_dict': cate_disp_dict,
        'is_logged_in': request.user.is_authenticated,
        'username': request.user.username,
        'email': request.user.email,
    }

    return render(request, 'client/fitting.html', context)

def e_handler401(request):
    return redirect("/accounts/login/")