from django.http import JsonResponse
from common.constants import Result, Message

def success_json_response(message = None, *args, **kwargs):
    if message:
        response_data = {Result(): Result.SUCCESS, Message(): message}
    else:
        response_data = {Result(): Result.SUCCESS}
    return JsonResponse(response_data, *args, **kwargs)

def failure_json_response(message = None, *args, **kwargs):
    if message:
        response_data = {Result(): Result.FAILURE, Message(): message}
    else:
        response_data = {Result(): Result.FAILURE}
    return JsonResponse(response_data, *args, **kwargs)
