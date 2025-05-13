from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    display_name = models.CharField(max_length=63)
    email = models.EmailField()

    def __str__(self):
        return self.display_name


class Gallery(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='article_images/')
    caption = models.CharField(max_length=255, blank=True)
