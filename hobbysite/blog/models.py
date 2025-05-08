"""
Defines ArticleCategory and Article models.
"""

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class ArticleCategory(models.Model):
    """Model for an article category with name and description."""
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class Article(models.Model):
    """Model for an article."""
    title = models.CharField(max_length=255)
    author = author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='article'
    )
    entry = models.TextField()
    header_image = models.ImageField(upload_to='images/', null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        """Returns the URL to access the detail view of each article."""
        return reverse('blog:article_detail', args=[str(self.pk)])

class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=True,
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)