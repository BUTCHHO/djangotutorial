from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import user_creation_form, authentication_form
from django.shortcuts import render
from django.views import View

from .models import User

from common.constants import Message
from common.shortcuts import success_json_response, failure_json_response

from time import perf_counter

def check_logged_in_view(request):
    user = request.user
    if User.objects.filter(username=user.username).first():
        return success_json_response()
    return failure_json_response()

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/logout.html')

    def post(self, request):
        logout(request)
        return success_json_response()

class LoginView(View):
    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            return failure_json_response(Message.ACCOUNTS_USERNAME_PASSWORD_UNFILLED, status=422)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return success_json_response(Message.ACCOUNTS_SUCCESS_LOGGED_IN)
        else:
            return failure_json_response(Message.ACCOUNTS_WRONG_PSW_OR_USERNAME)


    def get(self, request):
        return render(request, 'accounts/login.html', {'form':authentication_form})

class CreateAccountView(View):
    def post(self, request):
        try:
            username=request.POST['username']
            password1=request.POST['password1']
            password2=request.POST['password2']
        except KeyError:
            return failure_json_response(Message.ACCOUNTS_USERNAME_PASSWORD_UNFILLED, status=422)
        if password1 != password2:
            return failure_json_response(Message.ACCOUNTS_PASSWORDS_MUST_BE_SAME, status=400)
        User.objects.create_user(
            username=username,
            password=password1
        )
        return success_json_response()

    def get(self, request):
        return render(request, 'accounts/create_account.html', {'form':user_creation_form})