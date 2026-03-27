from django.shortcuts import render
from django.core.paginator import Paginator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ObjectDoesNotExist


from accounts.models import User
from common.constants import Message
from common.shortcuts import failure_json_response, success_json_response
from .models import FriendRequest

class FriendsIndexView(LoginRequiredMixin, View):

    friends_query_offset = 10

    def get(self, request):
        user = request.user
        friends = user.friends.all()
        paginator = Paginator(friends, FriendsIndexView.friends_query_offset)
        page = request.GET['page']
        friends_page = paginator.page(page)
        return render(request, 'friends/index.html', {'friends':friends_page})


class SendFriendRequestView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        recipient_name = request.POST.get('recipient')
        if not recipient_name:
            return failure_json_response()
        try:
            recipient = User.objects.get(username=recipient_name)
        except ObjectDoesNotExist:
            return failure_json_response(Message.FRIENDS_USER_DONT_EXISTS)

        if user == recipient:
            return failure_json_response(Message.FRIENDS_CANT_SEND_REQUEST_TO_USER)

        if user.friends.filter(username=recipient.username).first() is not None:
            return failure_json_response(Message.FRIENDS_CANT_SEND_REQUEST_TO_USER)
        try:
            FriendRequest.objects.get(sender=user, recipient=recipient)
            return failure_json_response(Message.FRIENDS_REQUEST_ALREADY_SENT)
        except ObjectDoesNotExist:
            FriendRequest.objects.create(sender=user, recipient=recipient)
            return success_json_response()


