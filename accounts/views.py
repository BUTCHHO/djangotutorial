from django.contrib.auth import logout, login
from django.http import JsonResponse


def logout_view(request):
    logout(request)
    return JsonResponse({'l':'1'})
