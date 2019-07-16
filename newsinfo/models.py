from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class likedManager(models.Manager):
    def create_obj(self, user, category, country, author, image, date, source, url, title, description):
        news = self.create(user=user, category=category, country=country, author=author,
                           image=image, date=date, source=source, url=url, title=title, description=description)
        return news


class liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    category = models.CharField(max_length=20)
    country = models.CharField(max_length=2)
    author = models.CharField(max_length=50)
    image = models.URLField(max_length=400)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    source = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    objects = likedManager()
