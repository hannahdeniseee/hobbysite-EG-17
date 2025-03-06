"""
Defines ArticleCategory and Article models.
"""

from django.db import models
from django.urls import reverse

class ArticleCategory(models.Model):
    """Model for an article category with name and description."""
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return str(self.name)

class Article(models.Model):
    """Model for an article with a title, category, entry, and creation and update dates."""
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='article'
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        """Returns the URL to access the detail view of this recipe."""
        return reverse('blog:article_detail', args=[str(self.pk)])
    
