
from django.db.models import F
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment

from common.shortcuts import success_json_response, failure_json_response
from common.constants import Message, Result


class IndexView(ListView):
    template_name = "community/index.html"
    context_object_name = "posts"

    extra_context = {"no_posts_message": Message.COMMUNITY_NO_POSTS}
    queryset_offset = 5
    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:IndexView.queryset_offset]


class DetailView(View):
    def get(self,request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.is_pub_date_future():
            context = {"no_post_available_message": Message.COMMUNITY_NO_POSTS}
        else:
            post.views = F("views") + 1
            post.save()
            post.refresh_from_db()
            context = {"post":post}
        return render(request, "community/detail.html", context)


class LikeView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.is_pub_date_future():
            return failure_json_response(Message.COMMUNITY_NO_POSTS, status=404)
        post.likes = F("likes") + 1
        post.save()
        post.refresh_from_db()
        return JsonResponse({Result(): Result.SUCCESS, 'likes':post.likes})


class DislikeView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.is_pub_date_future():
            failure_json_response(Message.COMMUNITY_NO_POSTS, status=404)
        post.dislikes = F("dislikes") + 1
        post.save()
        return JsonResponse(
            {Result(): Result.SUCCESS,
             'dislikes':post.dislikes,
             },
        )


class CreateCommentView(LoginRequiredMixin, View):

    def post(self, request: HttpRequest, post_id):
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        if post.is_pub_date_future():
            return failure_json_response(Message.COMMUNITY_NO_POSTS, status=404)
        try:
            comment_content = request.POST['comment_content']
        except KeyError:
            return failure_json_response(Message.COMMUNITY_EMPTY_COMMENT_CONTENT, status=422)
        if comment_content == '':
            return failure_json_response(Message.COMMUNITY_EMPTY_COMMENT_CONTENT, status=422)
        comment = Comment(post=post, content=comment_content, pub_date=timezone.now(), author=user)
        comment.save()
        return success_json_response()