from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'header_image', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-box', }),
            'category': forms.Select(attrs={'class': 'categ-box', }),
            'entry': forms.Textarea(attrs={'class': 'comment-box', }),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'created_on', 'updated_on', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-box', }),
            'category': forms.Select(attrs={'class': 'categ-box', }),
            'entry': forms.Textarea(attrs={'class': 'comment-box', }),
        }
