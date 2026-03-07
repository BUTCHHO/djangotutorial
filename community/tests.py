from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from django.shortcuts import reverse

import datetime

from .models import Post, Comment

from .views import IndexView, DetailView

def create_post(days, title='post', content='post content', views=0, likes=0, dislikes=0):
    date = timezone.now() + timedelta(days=days)
    return Post.objects.create(title=title,
                               content=content,
                               pub_date=date,
                               views=views,
                               likes=likes,
                               dislikes=dislikes,

                            )

class PostIndexViewTests(TestCase):
    def test_future_posts_not_displayed(self):
        create_post(days=10)
        response = self.client.get(reverse('community:index'))
        self.assertContains(response, IndexView.no_posts_message)
