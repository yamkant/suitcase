from django.shortcuts import render, redirect
from rest_framework.views import APIView
from users.serializers import UserSerializer
from users.forms.join_form import UserJoinForm
from users.forms.login_form import UserLoginForm
from rest_framework.views import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

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