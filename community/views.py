from django.http import HttpResponse, Http404
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post

class IndexView(ListView):
    template_name = "community/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.order_by('-pub_date')[:5]

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.views = F("views") + 1
    post.save()
    context = {"post":post}
    return render(request, "community/detail.html", context)
