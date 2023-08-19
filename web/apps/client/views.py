from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from client.libs.custom_decorators import login_required

from products.models import Product

@require_http_methods(['GET'])
@login_required
def render_home(request):
    prod_list = Product.objects.filter()
    context = {'prod_list': prod_list}

    return render(request, 'client/home.html', context)
