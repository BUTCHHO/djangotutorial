from django.urls import path
from .views import IndexView, detail

app_name = 'community'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:post_id>/detail", detail, name="detail"),
]