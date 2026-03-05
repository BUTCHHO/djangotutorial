from django.http import HttpResponse, Http404
from django.db.models import F
from django.shortcuts import render

from .models import Post

def index(request):
    posts = Post.objects.order_by("-pub_date")[:5]
    context = {"posts": posts}
    return render(request, "community/index.html", context)

def detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Requested post does not exist")
    post.views = F("views") + 1
    post.save()
    context = {"post":post}
    return render(request, "community/detail.html", context)
