from django.db import models
from django.utils import timezone

from accounts.models import User

import datetime

class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=1024)
    pub_date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    author = models.ForeignKey('accounts.User', on_delete=models.SET(User.get_deleted_user))

    recent_days = 1

    def increment_view(self):
        self.views += 1
        self.save()

    def increment_likes(self):
        self.likes += 1
        self.save()

    def increment_dislikes(self):
        self.dislikes += 1
        self.save()

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(Post.recent_days)

    def is_pub_date_future(self):
        return self.pub_date > timezone.now()

    def get_rating(self):
        return self.likes - self.dislikes

class Comment(models.Model):
    post = models.ForeignKey(Post, models.CASCADE)
    content = models.CharField(max_length=256)
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('accounts.User', on_delete=models.SET(User.get_deleted_user))
