from django.db import models
from django.urls import reverse


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    class Meta:
        ordering = ['name']  # Sort categories by name in ascending order
        verbose_name_plural = "Article Categories"

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles'
    )
    entry = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki:article_detail', args=[self.pk])
