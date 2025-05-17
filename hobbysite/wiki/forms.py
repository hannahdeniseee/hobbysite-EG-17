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
    class Meta:
        model = Comment
        fields = ['entry', ]
        widgets = {
            'entry': forms.Textarea(label="Leave a comment:", attrs={'class': 'comment-box', })
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'entry', 'header_image', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-box', }),
            'category': forms.Select(attrs={'class': 'categ-box', }),
            'entry': forms.Textarea(attrs={'class': 'comment-box', }),
        }
