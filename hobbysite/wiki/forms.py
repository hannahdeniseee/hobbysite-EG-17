from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'entry', 'header_image', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-box', }),
            'category': forms.Select(attrs={'class': 'categ-box', }),
            'entry': forms.Textarea(attrs={'class': 'comment-box', }),
            'image': forms.ClearableFileInput(),  # allows deletion of image
        }


class CommentForm(forms.ModelForm):
    entry = forms.CharField(
        label="Leave a comment:",
        widget=forms.Textarea(attrs={'class': 'comment-box'})
    )

    class Meta:
        model = Comment
        fields = ['entry', ]


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'entry', 'header_image', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-box', }),
            'category': forms.Select(attrs={'class': 'categ-box', }),
            'entry': forms.Textarea(attrs={'class': 'comment-box', }),
        }
