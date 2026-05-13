from django.forms import ModelForm 
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re


class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'profile_picture',
            'password1',
            'password2'
        )

    def clean_password1(self):

        password = self.cleaned_data.get("password1")

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")

        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")

        if not re.search(r"[0-9]", password):
            raise forms.ValidationError("Password must contain at least one number.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError("Password must contain at least one special character.")

        return password



class EditProfileForm(forms.ModelForm):

    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput()
    )

    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "profile_picture"]


    def clean_new_password(self):

        password = self.cleaned_data.get("new_password")

        if password:

            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")

            if not re.search(r"[A-Z]", password):
                raise forms.ValidationError("Password must contain at least one uppercase letter.")

            if not re.search(r"[a-z]", password):
                raise forms.ValidationError("Password must contain at least one lowercase letter.")

            if not re.search(r"[0-9]", password):
                raise forms.ValidationError("Password must contain at least one number.")

            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                raise forms.ValidationError("Password must contain at least one special character.")

        return password