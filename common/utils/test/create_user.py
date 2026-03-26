from accounts.models import User

def create_user(username='testificate', password='psw'):
    return User.objects.create_user(username=username, password=password)