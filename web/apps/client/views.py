from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from client.libs.custom_decorators import login_required

from products.models import Product

# TODO: 기본 필터는 묶어서 전처리로 수행되도록 수정

@require_http_methods(['GET'])
@login_required
def render_home(request):
    prod_list = Product.objects.filter(user_id=request.user.id, is_deleted="N")

    cate_dict = {
        "UNDEFINED": 1,
        "PANTS": 2,
        "TOPS": 3,
        "SHOES": 4,
    }

    context = {
        'prod_list': prod_list,
        'cate_dict': cate_dict,
        'is_logged_in': request.user.is_authenticated,
        'username': request.user.username,
        'email': request.user.email,
    }

    return render(request, 'client/home.html', context)

@require_http_methods(['GET'])
@login_required
def render_fitting(request):
    prod_list = Product.objects.filter(user_id=request.user.id, is_deleted="N")
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
