from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema

from apps.users.serializers import UserSerializer
from apps.users.forms.join_form import UserJoinForm
from apps.users.forms.login_form import UserLoginForm

@extend_schema(
    exclude=True
)
class JoinAPIView(APIView):
    form_class = UserJoinForm
    template_name = 'accounts/join.html'
    serializer_class = UserSerializer

    def get(self, request):
        context = {}
        context['form'] = self.form_class()
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('/')
        context = {'form': form}
        return render(request, self.template_name, context)

@extend_schema(
    exclude=True
)
class LoginAPIView(APIView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    serializer_class = UserSerializer

    def get(self, request):
        context = {}
        context['form'] = self.form_class()
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
        context = {'form' : form}
        return render(request, self.template_name, context)