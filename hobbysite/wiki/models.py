from django.db import models
from django.urls import reverse
from user_management.models import Profile


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
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='wiki_articles'
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles'
    )
    entry = models.TextField(null=True)
    header_image = models.ImageField(upload_to='wiki/images/', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki:article_detail', args=[self.pk])


class Comment(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name= "wiki_comments"
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=False,
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']


class Gallery(models.Model):
    image = models.ImageField(
        upload_to='wiki/images/',
        blank=True,
        null=True
    )
    article = models.ForeignKey(
        'wiki.Article',
        on_delete=models.CASCADE,
        null=True,
    )
