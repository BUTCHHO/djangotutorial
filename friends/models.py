from django.db import models
from django.utils import timezone

class FriendRequest(models.Model):
    recipient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='friend_request_recipient')
    sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    send_date = models.DateTimeField(default=timezone.now)