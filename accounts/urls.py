from django.urls import path

from .views import LogoutView, LoginView, CreateAccountView

app_name = 'accounts'

urlpatterns = [
    path('logout', LogoutView.as_view(), name='logout'),
    path('login', LoginView.as_view(), name='login'),
    path('create_account', CreateAccountView.as_view(), name='create_account')
]