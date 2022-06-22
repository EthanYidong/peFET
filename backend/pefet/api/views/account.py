import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings

import bcrypt
import jwt

from ..models import User
from ..helpers import auth, json_data


@require_http_methods(['POST'])
@json_data(schema={
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"]
})
def signup(request, data):
    if User.objects.filter(email=data['email']).exists():
        return JsonResponse({'errors': ['User already exists']}, status=400)

    new_user = User(email=data['email'], password=bcrypt.hashpw(
        bytes(data['password'], 'utf-8'), bcrypt.gensalt()))

    new_user.save()

    encoded_jwt = jwt.encode({'sub': new_user.id},
                             settings.JWT_SECRET, algorithm='HS256')

    return JsonResponse({'token': encoded_jwt})


@require_http_methods(['POST'])
@json_data(schema={
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"]
})
def login(request, data):
    try:
        existing_user = User.objects.get(email=data['email'])
    except User.DoesNotExist:
        return JsonResponse({'errors': ['User with that email does not exist']}, status=401)

    if not bcrypt.checkpw(bytes(data['password'], 'utf-8'), existing_user.password):
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
