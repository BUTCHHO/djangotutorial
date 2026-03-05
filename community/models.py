from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=1024)
    pub_date = models.DateTimeField()
    views = models.IntegerField(default=0)

class Comment(models.Model):
    post = models.ForeignKey(Post, models.CASCADE)
    content = models.CharField(max_length=256)
    pub_date = models.DateTimeField()