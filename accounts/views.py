from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import user_creation_form, authentication_form
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from .models import User

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/logout.html')

    def post(self, request):
        logout(request)
        return JsonResponse({'result':'success'})

class LoginView(View):
    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            return JsonResponse({'result':'failure', 'message':"user name and password fiends must be filled"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'result': 'success', 'message':'successfully logged in'})
        else:
            return JsonResponse({'result':'failure','message':'wrong password or username'})

    def get(self, request):
        return render(request, 'accounts/login.html', {'form':authentication_form})

class CreateAccountView(View):
    def post(self, request):
        try:
            username=request.POST['username']
            password1=request.POST['password1']
            password2=request.POST['password2']
        except KeyError:
            return JsonResponse({'result':'failure', 'message':"user name and password fiends must be filled"}, status=422)
        if password1 != password2:
            return JsonResponse({'result':'failure','message':'password must be same'}, status=400)
        User.objects.create_user(
            username=username,
            password=password1
        )
        return JsonResponse({'result':'success'})

    def get(self, request):
        return render(request, 'accounts/create_account.html', {'form':user_creation_form})