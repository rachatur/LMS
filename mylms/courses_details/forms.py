from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )


class SignUpForm(UserCreationForm):
    # email = forms.EmailField(
    #     widget=forms.EmailInput()
    # )

    # The Meta class specifies the model to be used
    class Meta:
        # link the form with the custom user model, this form will create & modify instance of the model
        model = User
        fields = ['username', 'email', 'password1', 'password2']