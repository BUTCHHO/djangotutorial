from django.urls import path
from .views import FriendsIndexView, SendFriendRequestView


app_name = 'friends'

urlpatterns = [
    path('', FriendsIndexView.as_view(), name='index'),
    path('send_request', SendFriendRequestView.as_view(), name='send_request'),
    # path('accept_request', AcceptFriendRequestView.as_view(), name='accept_request'),
    # path('decline_request', DeclineFriendRequestView.as_view(), name='decline_request'),
    # path('cancel_request', CancelFriendRequestView.as_view(), name='cancel_request'),

]