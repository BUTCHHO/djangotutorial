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
    def test_future_post_not_displayed(self):
        create_post(days=10)
        response = self.client.get(reverse('community:index'))
        self.assertContains(response, IndexView.no_posts_message)

    def test_past_post_displayed(self):
        post = create_post(days=-10)
        response = self.client.get(reverse('community:index'))
        self.assertContains(response, post.title)
        self.assertEqual(list(response.context['posts']), [post])

    def test_lot_posts_displayed_within_offset(self):
        post_amount = 10
        posts = []
        for i in range(post_amount):
            post = create_post(-1, title=f'post_{i}')
            posts.append(post)
        response = self.client.get(reverse('community:index'))
        self.assertEqual(len(response.context['posts']), IndexView.queryset_offset)

class PostDetailViewTests(TestCase):
    def test_views_increment(self):
        post = create_post(-1)
        post_views_before = post.views
        response = self.client.get(reverse('community:detail', args=(post.id,)))
        post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.views, post_views_before+1)

    def test_future_post_not_displayed(self):
        post = create_post(1)
        response = self.client.get(reverse('community:detail', args=(post.id,)))
        self.assertContains(response, DetailView.no_post_available_message)

    def test_post_like_increment(self):
        post = create_post(-1)
        post_likes_before = post.likes
        response = self.client.post(reverse("community:like", args=(post.id,)))
        post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.likes, post_likes_before+1)

    def test_post_like_increment_being_displayed(self):
        post = create_post(-1)
        post_likes_before = post.likes
        response = self.client.post(reverse('community:like', args=(post.id,)))
        post.refresh_from_db()
        self.assertEqual(response.context['post'].likes, post_likes_before+1)

    def test_post_dislike_increment(self):
        post = create_post(-1)
        post_dislikes_before = post.dislikes
        response = self.client.post(reverse("community:dislike", args=(post.id,)))
        post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.dislikes, post_dislikes_before+1)

    def test_post_dislike_increment_being_displayed(self):
        post = create_post(-1)
        post_dislikes_before = post.dislikes
        response = self.client.post(reverse('community:dislike', args=(post.id,)))
        post.refresh_from_db()
        self.assertEqual(response.context['post'].dislikes, post_dislikes_before+1)