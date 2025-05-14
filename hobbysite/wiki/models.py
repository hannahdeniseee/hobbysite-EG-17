from django.db import models
from django.urls import reverse
from user_management.models import Profile


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    class Meta:
        ordering = ['name']  # Sort categories by name in ascending order (a to z)
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
    header_image = models.ImageField(upload_to='wiki/images/')
    image = models.ImageField(upload_to='wiki/images', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on'] # Sort articles by date in descending order (newest first)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki:article_detail', args=[self.pk])


class Comment(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="wiki_comments"
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
        ordering = ['created_on'] # Sort comments by date in ascending order (oldest first)
