# accounts forms.py
from typing import Any, Optional
from django import forms
from django.forms.widgets import Widget
import unicodedata

class EmailFormField(forms.EmailField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))
    
    def widget_attrs(self, widget: Widget) -> Any:
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'email',
            'placeholder': '이메일',
        }

class PasswordFormField(forms.CharField):
    def widget_attrs(self, widget: Widget) -> Any:
        return {
            'autocomplete': 'new-password',
            'placeholder': "비밀번호",
            'strip': False,
            **super().widget_attrs(widget),
        }

class PhoneFormField(forms.CharField):
    def widget_attrs(self, widget: Widget) -> Any:
        return {
            **super().widget_attrs(widget),
            'autocomplete': 'new-password',
            'type': 'number',
            'placeholder': '전화번호',
        }

class UsernameFormField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))
    
    def widget_attrs(self, widget: Widget) -> Any:
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'username',
            'placeholder': '이름',
        }
