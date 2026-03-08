from django.test import TestCase

from .models import User

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