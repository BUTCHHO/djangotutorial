from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    @classmethod
    def get_deleted_user(cls):
        user, _is_created = cls.objects.get_or_create(
            username='Deleted user',
            defaults={
                'first_name':'Deleted',
                'last_name':'User',
                'email':'deleted_user@deleted_user.com',
                'is_active':False
            }
        )
        return user
