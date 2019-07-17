from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class likedManager(models.Manager):
    def create_obj(self, user, category, country, author, image, date, source, url, title, description):
        news = self.create(user=user, category=category, country=country, author=author,
                           image=image, date=date, source=source, url=url, title=title, description=description)
        return news


class liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    category = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=2)
    author = models.CharField(max_length=50, null=True)
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
