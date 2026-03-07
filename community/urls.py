from django.urls import path
from .views import IndexView, DetailView, LikeView, DislikeView

app_name = 'community'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:post_id>/detail", DetailView.as_view(), name="detail"),
    path('<int:post_id>/like', LikeView.as_view(), name='like'),
    path('<int:post_id>/dislike', DislikeView.as_view(), name='dislike'),
]