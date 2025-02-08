from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from .models import CustomUser

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username/Email")

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True)

class CustomPasswordChangeForm(PasswordChangeForm):
    pass