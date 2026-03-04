from django.urls import path
from .views import index, detail

app_name = 'community'

urlpatterns = [
    path("", index, name="index"),
    path("<int:post_id>/detail", detail, name="detail"),
]