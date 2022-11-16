from dataclasses import fields
from django import forms

from apps.authentication.models import Profile


class EditProfileForm(forms.ModelForm):
    # email = forms.
    class Meta:
        model = Profile
        # fields = ('first_name', 'last_name', 'address')
        fields = "__all__"

