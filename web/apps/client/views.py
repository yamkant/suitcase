from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from client.libs.custom_decorators import login_required

from products.models import Product

@require_http_methods(['GET'])
@login_required
def render_home(request):
    prod_list = Product.objects.filter()
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
    }

    return render(request, 'client/home.html', context)
