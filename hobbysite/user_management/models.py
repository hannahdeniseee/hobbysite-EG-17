"""
This is the models file to specify the fields and related methods
for the models used in the user_management app.
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Represents a profile which extends the user model.

    Includes fields for user, display_name, and email.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    display_name = models.CharField(max_length=63)
    email = models.EmailField()

    def __str__(self):
        return self.display_name
