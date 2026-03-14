from django.test import TestCase
from django.shortcuts import reverse

from .models import User

from constants import Message, Result


def create_user(username, email='johndoe@example.com'):
    return User.objects.create(
        username=username,
        first_name='testificate',
        last_name='user',
        email=email
    )

class UserModelTest(TestCase):
    def test_get_deleted_user_returns_deleted_user(self):
        deleted_user = User.get_deleted_user()
        self.assertEqual(deleted_user.username, 'Deleted user')

    def test_get_deleted_user_return_deleted_user_if_lot_of_users(self):
        users_amount = 20
        for i in range(users_amount):
            create_user(username=f'user_{i}')
        deleted_user = User.get_deleted_user()
        self.assertEqual(deleted_user.username, 'Deleted user')

    def test_get_testificate_user_returns_testificate(self):
        testificate_user = User.get_testificate_user()
        self.assertEqual(testificate_user.username, 'Testificate user')

class CreateAccountVIewTest(TestCase):
    def test_user_is_created_if_all_fields_filled_with_valid_data(self):
        username = 'user_name'
        password = 'psw_123123'
        response = self.client.post(reverse('accounts:create_account'), data={'username':username, 'password1':password, 'password2':password})
        self.assertJSONEqual(response.content, {Result(): Result.SUCCESS})
        user = User.objects.filter(username=username).first()
        self.assertIsNotNone(user)

    def test_user_is_not_created_if_passwords_not_same(self):
        username = 'user_name'
        password1 = 'psw_123123'
        password2 = 'psw_1231233'
        response = self.client.post(reverse('accounts:create_account'), data={'username':username, 'password1':password1, 'password2':password2})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {Result():Result.FAILURE, Message():Message.ACCOUNTS_PASSWORDS_MUST_BE_SAME})
        user = User.objects.filter(username=username).first()
        self.assertIsNone(user)

    def test_user_is_not_created_if_fields_unfilled(self):
        response = self.client.post(reverse('accounts:create_account'))
        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(response.content, {Result():Result.FAILURE, Message():Message.ACCOUNTS_USERNAME_PASSWORD_UNFILLED})
        users = User.objects.all()
        self.assertFalse(users.exists())