from common.utils.test.create_user import create_user

def login_client(client):
    user = create_user()
    client.login(username=user.username, password='psw')
    return user
