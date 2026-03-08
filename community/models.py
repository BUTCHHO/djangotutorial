from django.db import models
from django.utils import timezone
import datetime

class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=1024)
    pub_date = models.DateTimeField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    recent_days = 1

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(Post.recent_days)

    def is_pub_date_future(self):
        return self.pub_date > timezone.now()

    def get_rating(self):
        return self.likes - self.dislikes

class Comment(models.Model):
    post = models.ForeignKey(Post, models.CASCADE)
    content = models.CharField(max_length=256)
    pub_date = models.DateTimeField()