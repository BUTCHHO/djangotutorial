
from django.db.models import F
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment

class IndexView(ListView):
    template_name = "community/index.html"
    context_object_name = "posts"

    no_posts_message = "No posts are available"
    extra_context = {"no_posts_message": no_posts_message}
    queryset_offset = 5
    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:IndexView.queryset_offset]


class DetailView(View):
    no_post_available_message = 'No posts available.'
    def get(self,request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.is_pub_date_future():
            context = {"no_post_available_message": DetailView.no_post_available_message}
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
            return JsonResponse({'result':'failure','message':'No posts available to like'}, status=404)
        post.likes = F("likes") + 1
        post.save()
        post.refresh_from_db()
        response_data = {
            'result':'success',
            'likes':post.likes
        }
        return JsonResponse(response_data)


class DislikeView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.is_pub_date_future():
            return JsonResponse({'result':'failure','message':'No posts available to dislike'}, status=404)
        post.dislikes = F("dislikes") + 1
        post.save()
        return JsonResponse(
            {'result':'success',
             'dislikes':post.dislikes,
             }
        )


class CreateCommentView(LoginRequiredMixin, View):
    empty_comment_content_message = "Comment content cant be empty"
    cant_comment_future_posts_message = 'No posts available to comment'
    def post(self, request: HttpRequest, post_id):
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        if post.is_pub_date_future():
            return JsonResponse({'result':'failure','message':CreateCommentView.cant_comment_future_posts_message}, status=404)
        try:
            comment_content = request.POST['comment_content']
        except KeyError:
            return JsonResponse({'result':'failure', 'message': CreateCommentView.empty_comment_content_message})
        if comment_content == '':
            return JsonResponse({'result':'failure', 'message': CreateCommentView.empty_comment_content_message})
        comment = Comment(post=post, content=comment_content, pub_date=timezone.now(), author=user)
        comment.save()
        return JsonResponse({'result':'success'})