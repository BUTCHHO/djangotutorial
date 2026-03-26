from django.urls import path

from .views import LogoutView, LoginView, CreateAccountView, check_logged_in_view

app_name = 'accounts'

urlpatterns = [
    path('logout', LogoutView.as_view(), name='logout'),
    path('login', LoginView.as_view(), name='login'),
    path('create_account', CreateAccountView.as_view(), name='create_account'),
    path('_check_login', check_logged_in_view, name='check_login')
]
