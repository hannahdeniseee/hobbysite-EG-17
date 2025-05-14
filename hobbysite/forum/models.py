"""
This is the models file to specify the fields, ordering, and related methods
for the different models used in the Forum app.
"""

from django.db import models
from django.urls import reverse
from user_management.models import Profile


class ThreadCategory(models.Model):
    """
    Represents a category for the threads to be posted.

    Includes fields for name and description.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Thread Categories"

    def __str__(self):
        return self.name


class Thread(models.Model):
    """
    Represents a thread posted in the forum.

    Includes fields for name, author, category, entry,
    image, created_on, and updated_on.
    """
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
    )
    category = models.ForeignKey(
        ThreadCategory,
        on_delete=models.SET_NULL,
        null=True,
    )
    entry = models.TextField()
    image = models.ImageField(upload_to='forum/images/', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:thread-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    """
    Represents a comment under a specific thread in the Forum.

    Includes fields for author, thread (under which it was commented),
    entry, created_on, and updated_on.
    """
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
    )
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        null=False,
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']
