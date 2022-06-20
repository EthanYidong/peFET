import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings

import bcrypt
import jwt

from ..models import User
from ..helpers import auth


@require_http_methods(['POST'])
def signup(request):
    content = json.loads(request.body)

    if User.objects.filter(email=content['email']).exists():
        return JsonResponse({'errors': ['User already exists']}, status=401)

    new_user = User(email=content['email'], password=bcrypt.hashpw(
        bytes(content['password'], 'utf-8'), bcrypt.gensalt()))

    new_user.save()

    encoded_jwt = jwt.encode({'sub': new_user.id},
                             settings.JWT_SECRET, algorithm='HS256')

    return JsonResponse({'token': encoded_jwt})


@require_http_methods(['POST'])
def login(request):
    content = json.loads(request.body)

    try:
        existing_user = User.objects.get(email=content['email'])
    except User.DoesNotExist:
        return JsonResponse({'errors': ['User with that email does not exist']}, status=401)

    if not bcrypt.checkpw(bytes(content['password'], 'utf-8'), existing_user.password):
        return JsonResponse({'errors': ['Password is incorrect']}, status=401)

    encoded_jwt = jwt.encode(
        {'sub': existing_user.id}, settings.JWT_SECRET, algorithm='HS256')

    return JsonResponse({'token': encoded_jwt})


@require_http_methods(['GET'])
def validate(request):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    existing_user = User.objects.get(id=claims['sub'])

    return JsonResponse({'id': existing_user.id})
