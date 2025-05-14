"""
Django views for handling user inputs.
"""

from django import forms
from .models import Article, Comment, Gallery


class ArticleForm(forms.ModelForm):
    """Form to create an article."""

    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'header_image', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-box', }),
            'category': forms.Select(attrs={'class': 'categ-box', }),
            'entry': forms.Textarea(attrs={'class': 'comment-box', }),
        }


class UpdateForm(forms.ModelForm):
    """Form to edit an article."""

    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'header_image', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-box', }),
            'category': forms.Select(attrs={'class': 'categ-box', }),
            'entry': forms.Textarea(attrs={'class': 'comment-box', }),
        }


class CommentForm(forms.ModelForm):
    """Form to comment on an article."""

    class Meta:
        model = Comment
        fields = ['entry', ]
        widgets = {
            'entry': forms.Textarea(attrs={'class': 'comment-box', })
        }


class GalleryForm(forms.ModelForm):
    """Form to upload images in the gallery."""

    class Meta:
        model = Gallery
        fields = ['image', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].widget.attrs.update({"multiple": "true"})
