from django.db import models
from django.utils import timezone

import datetime

from accounts.models import User

class Question(models.Model):
    text = models.CharField(max_length=128)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    author = models.ForeignKey('accounts.User', on_delete=models.SET(User.get_deleted_user))

    def __str__(self):
        return self.text

    recent_days = 1
    min_choices = 2

    def was_published_recently(self):
        time_now = timezone.now()
        return time_now >= self.pub_date >= time_now - datetime.timedelta(days=Question.recent_days)

    def is_pub_date_future(self):
        if self.pub_date > timezone.now():
            return True
        return False


class Choice(models.Model):
    question = models.ForeignKey(Question, models.CASCADE)
    choice_text = models.CharField(max_length=64)

    @property
    def votes(self):
        return self.user_set.count()

    def __str__(self):
        return self.choice_text