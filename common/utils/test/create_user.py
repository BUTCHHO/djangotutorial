from accounts.models import User

def create_user():
    return User.objects.create_user('testificate', password='psw')


