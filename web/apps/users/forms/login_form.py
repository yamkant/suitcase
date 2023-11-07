from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.shortcuts import get_object_or_404

from apps.users.forms.fields import PasswordFormField, UsernameFormField
from apps.users.models import User

class UserLoginForm(forms.ModelForm):
    login_username = UsernameFormField(label="username",)
    password = PasswordFormField(label="password", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        try:
            username = cleaned_data.get('login_username')
            password = cleaned_data.get('password')
            if not username or not password:
                raise KeyError
        except KeyError:
            raise forms.ValidationError("아이디 혹은 비밀번호를 모두 입력해주세요.")
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("가입되지 않은 유저입니다.")
        if not check_password(password, user.password):
            self.add_error('login_username', '비밀번호를 잘못 입력했습니다.')
        self.user_cache = authenticate(
            self.request, username=username, password=password
        )
        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache
            
    class Meta:
        model = User
        fields = ("login_username", "password",)