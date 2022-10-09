from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, SantasList


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2"
            ]



class SantasListForm(forms.ModelForm):
    class Meta:
        model = SantasList
        fields = [
            "name",
            "email",
        ]