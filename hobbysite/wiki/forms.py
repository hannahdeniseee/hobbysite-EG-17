from django import forms
from .models import Article, Comment, Gallery


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'image', ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry', ]


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'image', ]


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].widget.attrs.update({"multiple": "true"})
