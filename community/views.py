from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from django.shortcuts import reverse
from django.utils import timezone

from .models import Post

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


class LikeView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.is_pub_date_future():
            return HttpResponse('No posts available to like', status=404)
        post.likes = F("likes") + 1
        post.save()
        post.refresh_from_db()
        return render(request, 'community/detail.html',{'post':post})

class DislikeView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.is_pub_date_future():
            return HttpResponse('No posts available to dislike', status=404)
        post.dislikes = F("dislikes") + 1
        post.save()
        post.refresh_from_db()
        return render(request, 'community/detail.html',{'post':post})