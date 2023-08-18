from django.shortcuts import render, redirect
from rest_framework.views import APIView
from users.forms.join_form import UserJoinForm
from rest_framework.views import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

class JoinAPIView(APIView):
    form_class = UserJoinForm
    template_name = 'accounts/join.html'

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