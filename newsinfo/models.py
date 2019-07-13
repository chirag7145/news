from django.db import models
from django.contrib.auth.models import User
# Create your models here.


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
