

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

# from . models import Posts
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            }
        ))

    def clean(self):
        if self.is_valid():
            email    = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Incorrect Email / Password please try again.")

    def get_user(self):
   
        return authenticate(
                email   =self.cleaned_data.get('email', '').lower().strip(),
                password =self.cleaned_data.get('password', ''),
        )    



class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password Check"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def get_user(self):
   
        return authenticate(
                email=self.cleaned_data.get('email', '').lower().strip(),
                password=self.cleaned_data.get('password', ''),
        )    
        

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True)


class SetPasswordForms(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)
        
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2