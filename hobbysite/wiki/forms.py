from django import forms
from .models import Article, Comment, Gallery


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'entry', 'header_image', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-box', }),
            'entry': forms.Textarea(attrs={'class': 'comment-box', }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry', ]
        widgets = {
            'entry': forms.Textarea(attrs={'class': 'comment-box', })
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'entry', 'header_image', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-box', }),
            'entry': forms.Textarea(attrs={'class': 'comment-box', }),
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].widget.attrs.update({"multiple": "true"})
