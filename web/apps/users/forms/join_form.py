from django import forms
from users.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import  password_validation
from django.core.validators import MaxLengthValidator, RegexValidator
from rest_framework.validators import UniqueValidator
from users.forms.fields import UsernameFormField, PasswordFormField, EmailFormField, PhoneFormField
from users.serializers import UserCreateSerializer

class UserJoinForm(forms.ModelForm):
    email = EmailFormField(label="email", validators=[
        UniqueValidator,
        RegexValidator(
            regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            message="숫자, 영어, _, @ 만을 이용해서 작성해주세요."
        )
    ])
    password = PasswordFormField(label="password", widget=forms.PasswordInput)
    password2 = PasswordFormField(
        label="password check",
        widget=forms.PasswordInput()
    )
    username = UsernameFormField(label="username", validators=[
        MaxLengthValidator(50, message="50자 이내로 입력해주세요.")]
    )
    phone = PhoneFormField(label="phone", validators=[
        RegexValidator(
            regex=r'^[0-9]{9,11}$',
            message="숫자만을 이용하여, 9-11자 이내로 입력해주세요."
        )
    ])

    class Meta:
        model = User
        fields = ("email", "password", "password2", "username", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " *" 
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password(self):
        data = self.cleaned_data['password']
        password_validation.validate_password(data, self.instance)
        return data

    def clean_password2(self):
        try:
            data1 = self.cleaned_data['password']
        except KeyError:
            return ""
        data2 = self.cleaned_data['password2']
        if data1 != data2:
            self.add_error('password2', ValidationError("비밀번호가 일치하지 않습니다."))
        return data2
    
    def save(self, commit=True):
        new_user = super(UserJoinForm, self).save(commit=False)
        serializer = UserCreateSerializer(data=self.cleaned_data)
        if commit and serializer.is_valid(raise_exception=True):
            new_user = serializer.create(self.cleaned_data)
        return new_user