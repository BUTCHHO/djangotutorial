from django.urls import path
from .views import IndexView, DetailView

app_name = 'community'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:post_id>/detail", DetailView.as_view(), name="detail"),
]