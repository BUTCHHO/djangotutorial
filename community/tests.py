from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from django.shortcuts import reverse

from .models import Post, Comment

from .views import IndexView, DetailView,CreateCommentView

from accounts.models import User

from common.utils.test.login_client import login_client
from common.constants import Result, Message


def create_post(days, title='post', content='post content', views=0, likes=0, dislikes=0):
    date = timezone.now() + timedelta(days=days)
    return Post.objects.create(title=title,
                               content=content,
                               pub_date=date,
                               views=views,
                               likes=likes,
                               dislikes=dislikes,
                               author=User.get_testificate_user(),
                            )

def create_comment(post, days, content='comment content'):
    pub_date = timezone.now() + timedelta(days=days)
    return Comment.objects.create(
        post=post,
        content=content,
        pub_date=pub_date,
        author=User.get_testificate_user(),
    )


class PostModelTests(TestCase):
    def test_rating_negative_if_more_dislikes(self):
        likes = 10
        dislikes = likes + 10
        post = create_post(-1, likes=likes,dislikes=dislikes)
        rating = post.get_rating()
        self.assertLess(rating, 0)

    def test_rating_positive_if_more_likes(self):
        likes = 10
        dislikes = likes // 2
        post = create_post(-1, likes=likes,dislikes=dislikes)
        rating = post.get_rating()
        self.assertGreater(rating, 0)

    def test_rating_is_zero_if_likes_equal_dislikes(self):
        likes = 10
        dislikes = likes
        post = create_post(-1, likes=likes, dislikes=dislikes)
        rating = post.get_rating()
        self.assertEqual(rating, 0)

    def test_was_published_recently_with_future_post(self):
        post = create_post(10)
        self.assertFalse(post.was_published_recently())

    def test_was_published_recently_with_old_post(self):
        post = create_post(-Post.recent_days-1)
        self.assertFalse(post.was_published_recently())

    def test_was_published_recently_with_recent_post(self):
        post = create_post(-Post.recent_days+1)
        self.assertTrue(post.was_published_recently())

class PostIndexViewTests(TestCase):
    def test_future_post_not_displayed(self):
        create_post(days=10)
        response = self.client.get(reverse('community:index'))
        self.assertContains(response, Message.COMMUNITY_NO_POSTS)

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
        self.assertContains(response, Message.COMMUNITY_NO_POSTS)

    def test_post_like_increment(self):
        post = create_post(-1)
        post_likes_before = post.likes
        login_client(self.client)
        response = self.client.post(reverse("community:like", args=(post.id,)))
        post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.likes, post_likes_before+1)

    def test_post_like_increment_being_displayed(self):
        post = create_post(-1)
        post_likes_before = post.likes
        login_client(self.client)
        response = self.client.post(reverse('community:like', args=(post.id,)))
        post.refresh_from_db()
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertJSONEqual(response.content, {Result():Result.SUCCESS, 'likes':post_likes_before+1})
        response_after_like = self.client.get(reverse('community:detail', args=(post.id,)))
        self.assertEqual(response_after_like.context['post'].likes, post_likes_before+1)

    def test_post_dislike_increment(self):
        post = create_post(-1)
        post_dislikes_before = post.dislikes
        login_client(self.client)
        response = self.client.post(reverse("community:dislike", args=(post.id,)))
        post.refresh_from_db()
        self.assertJSONEqual(response.content,{Result():Result.SUCCESS, 'dislikes':post_dislikes_before+1})
        self.assertEqual(post.dislikes, post_dislikes_before+1)

    def test_post_dislike_increment_being_displayed(self):
        post = create_post(-1)
        post_dislikes_before = post.dislikes
        login_client(self.client)
        response = self.client.post(reverse('community:dislike', args=(post.id,)))
        post.refresh_from_db()
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertJSONEqual(response.content,{Result():Result.SUCCESS, 'dislikes':post_dislikes_before+1})
        response_after_dislike = self.client.get(reverse('community:detail', args=(post.id,)))
        self.assertEqual(response_after_dislike.context['post'].dislikes, post_dislikes_before+1)
class CommentCreationViewTest(TestCase):
    def test_new_comment_being_displayed(self):
        post = create_post(-1)
        comment_content = 'new comment'
        login_client(self.client)
        response = self.client.post(reverse('community:create_comment', args=(post.id,)),data={'comment_content': comment_content})
        post.refresh_from_db()
        self.assertJSONEqual(response.content, {Result(): Result.SUCCESS})
        self.assertEqual(post.comment_set.count(), 1)

    def test_future_posts_are_not_commentable(self):
        post = create_post(1)
        comment_content = 'comment for future post'
        login_client(self.client)
        response = self.client.post(reverse('community:create_comment', args=(post.id,)),data={'comment_content':comment_content})
        post.refresh_from_db()
        self.assertEqual(post.comment_set.count(), 0)
        self.assertEqual(response.status_code, 404)
        self.assertNotContains(response, comment_content, status_code=404)
        self.assertContains(response, Message.COMMUNITY_NO_POSTS, status_code=404)

    def test_error_message_displayed_if_comment_content_empty(self):
        post = create_post(-1)
        login_client(self.client)
        response = self.client.post(reverse('community:create_comment', args=(post.id,)))
        post.refresh_from_db()
        self.assertEqual(post.comment_set.count(), 0)
        self.assertContains(response, Message.COMMUNITY_EMPTY_COMMENT_CONTENT, status_code=422)

    def test_cant_comment_if_not_logged(self):
        post = create_post(-1)
        response = self.client.post(reverse('community:create_comment', args=(post.id,)), data={'comment_content':'content'})
        post.refresh_from_db()
        self.assertEqual(post.comment_set.count(), 0)
        self.assertEqual(response.status_code, 302)
        login_page_redirect_response = self.client.get(response.url)
        self.assertContains(login_page_redirect_response, 'login')