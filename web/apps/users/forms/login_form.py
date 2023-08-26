from django import forms
from users.forms.fields import EmailFormField, PasswordFormField
from users.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.shortcuts import get_object_or_404

class UserLoginForm(forms.ModelForm):
    login_email = EmailFormField(label="email")
    password = PasswordFormField(label="password", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        try:
            email = cleaned_data.get('login_email')
            password = cleaned_data.get('password')
            if not email or not password:
                raise KeyError
        except KeyError:
            raise forms.ValidationError("아이디 혹은 비밀번호를 모두 입력해주세요.")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("가입되지 않은 이메일입니다.")
        if not check_password(password, user.password):
            self.add_error('login_email', '비밀번호를 잘못 입력했습니다.')
        self.user_cache = authenticate(
            self.request, email=email, password=password
        )
        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache
            
    class Meta:
        model = User
        fields = ("login_email", "password",)