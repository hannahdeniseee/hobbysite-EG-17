from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user_management.models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    display_name = forms.CharField(required=True, max_length=63)

    class Meta:
        model = User
        fields = ("username", "email", "display_name", "password1",
                  "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "display_name": self.cleaned_data["display_name"],
                    "email": user.email,
                }
            )
        return user
