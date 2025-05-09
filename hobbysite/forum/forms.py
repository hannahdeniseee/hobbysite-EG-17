from django import forms
from .models import Comment, Thread


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry', ]
        widgets = {
            'entry': forms.Textarea(attrs={'class': 'custom-comment-box', })
        }


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'category', 'entry', 'image', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom-title-box', }),
            'category': forms.Select(attrs={'class': 'custom-categ-box', }),
            'entry': forms.Textarea(attrs={'class': 'custom-comment-box', }),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'category', 'entry', 'image', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom-title-box', }),
            'category': forms.Select(attrs={'class': 'custom-categ-box', }),
            'entry': forms.Textarea(attrs={'class': 'custom-comment-box', }),
        }
