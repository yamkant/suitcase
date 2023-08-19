from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from client.libs.custom_decorators import login_required

@require_http_methods(['GET'])
@login_required
def render_home(request):
    context = {}
    return render(request, 'client/home.html', context)
