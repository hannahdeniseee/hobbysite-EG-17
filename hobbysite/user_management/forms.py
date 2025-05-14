"""
This is the forms file to specify the different types of forms
used in the user_management app.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile


class CustomLoginForm(AuthenticationForm):
    """
    Form for logging into the account of the user.

    It includes fields for username and password.
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',  'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for editing the user's profile.

    It only includes a field for the display_name.
    """
    class Meta:
        model = Profile
        fields = ['display_name']
