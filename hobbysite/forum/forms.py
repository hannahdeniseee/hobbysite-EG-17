"""
This is the forms file to specify the different types of forms
used in the Forum app.
"""

from django import forms
from .models import Comment, Thread


class CommentForm(forms.ModelForm):
    """
    Form for commenting on threads in the Forum.

    It only includes a field for entry because the other fields
    are automatically set. The css for this form is also set here.
    """
    class Meta:
        model = Comment
        fields = ['entry', ]
        widgets = {
            'entry': forms.Textarea(attrs={'class': 'custom-comment-box', })
        }


class ThreadForm(forms.ModelForm):
    """
    Form for creating new threads in the Forum.

    It includes fields for title, category, entry, and image only
    because the other fields are automatically set.
    The css for this form is also set here.
    """
    class Meta:
        model = Thread
        fields = ['title', 'category', 'entry', 'image', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom-title-box', }),
            'category': forms.Select(attrs={'class': 'custom-categ-box', }),
            'entry': forms.Textarea(attrs={'class': 'custom-comment-box', }),
        }


class UpdateForm(forms.ModelForm):
    """
    Form for updating the user's previously created threads in the Forum.

    It includes fields for title, category, entry, and image only
    because the other fields are automatically set or not editable.
    The css for this form is also set here.
    """
    class Meta:
        model = Thread
        fields = ['title', 'category', 'entry', 'image', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom-title-box', }),
            'category': forms.Select(attrs={'class': 'custom-categ-box', }),
            'entry': forms.Textarea(attrs={'class': 'custom-comment-box', }),
        }
