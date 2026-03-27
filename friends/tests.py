from django.test import TestCase
from django.shortcuts import reverse

from common.constants import Result, Message
from common.utils.test import create_user, login_client

from friends.models import FriendRequest


class SendFriendRequestViewTests(TestCase):
    def test_request_is_created_if_valid(self):
        recipient = create_user('recipient')
        sender = login_client(self.client)
        response = self.client.post(reverse('friends:send_request'), {'recipient': recipient.username})
        self.assertJSONEqual(response.content, {Result():Result.SUCCESS})
        self.assertTrue(FriendRequest.objects.filter(sender=sender, recipient=recipient).exists())

    def test_request_is_not_created_if_recipient_dont_exists(self):
        sender = login_client(self.client)
        fake_recipient = 'dedo123'
        response = self.client.post(reverse('friends:send_request'), {'recipient': fake_recipient})
        self.assertJSONEqual(response.content, {Result(): Result.FAILURE, Message(): Message.FRIENDS_USER_DONT_EXISTS})
        self.assertFalse(FriendRequest.objects.filter(sender=sender).exists())

    def test_request_is_not_created_if_recipient_is_sender(self):
        sender = login_client(self.client)
        response = self.client.post(reverse('friends:send_request'), {'recipient': sender.username})
        self.assertJSONEqual(response.content, {Result(): Result.FAILURE, Message(): Message.FRIENDS_CANT_SEND_REQUEST_TO_USER})
        self.assertFalse(FriendRequest.objects.filter(sender=sender).exists())

    def test_request_is_not_created_if_request_already_sent(self):
        recipient = create_user('recipient')
        sender = login_client(self.client)
        response = self.client.post(reverse('friends:send_request'), {'recipient': recipient.username})
        self.assertJSONEqual(response.content, {Result():Result.SUCCESS})
        self.assertTrue(FriendRequest.objects.filter(sender=sender, recipient=recipient).exists())
        response = self.client.post(reverse('friends:send_request'), {'recipient': recipient.username})
        self.assertJSONEqual(response.content, {Result():Result.FAILURE, Message(): Message.FRIENDS_REQUEST_ALREADY_SENT})
        self.assertEqual(FriendRequest.objects.filter(sender=sender).count(), 1)

    def test_request_is_not_created_if_users_already_friends(self):
        sender = login_client(self.client)
        recipient = create_user('recipient')
        sender.friends.add(recipient)
        response = self.client.post(reverse('friends:send_request'), {'recipient': recipient.username})
        self.assertJSONEqual(response.content, {Result():Result.FAILURE, Message():Message.FRIENDS_CANT_SEND_REQUEST_TO_USER})
        self.assertFalse(FriendRequest.objects.filter(sender=sender).exists())
