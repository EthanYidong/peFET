from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings

import json
import bcrypt
import jwt

from ..models import User

@require_http_methods(['POST'])
def signup(request):
  content = json.loads(request.body)

  if User.objects.filter(email=content['email']).exists():
    return JsonResponse({'errors': ['User already exists']}, status=401)
  
  new_user = User(email=content['email'], password=bcrypt.hashpw(bytes(content['password'], 'utf-8'), bcrypt.gensalt()))

  new_user.save()

  encoded_jwt = jwt.encode({'sub': new_user.id}, settings.JWT_SECRET, algorithm="HS256")

  return JsonResponse({'token': encoded_jwt})

@require_http_methods(['POST'])
def login(request):
  content = json.loads(request.body)

  existing_user = User.objects.filter(email=content['email'])

  if not existing_user.exists():
    return JsonResponse({'errors': ['User with that email does not exist']}, status=401)

  if not bcrypt.checkpw(bytes(content['password'], 'utf-8'), existing_user.first().password):
    return JsonResponse({'errors': ['Password is incorrect']}, status=401)

  encoded_jwt = jwt.encode({'sub': existing_user.first().email}, settings.JWT_SECRET, algorithm="HS256")

  return JsonResponse({'token': encoded_jwt})

@require_http_methods(['POST'])
def validate(request):
  content = json.loads(request.body)

  try:
    claims = jwt.decode(content['token'], settings.JWT_SECRET, ['HS256'])
  except:
    return JsonResponse({'errors': ['Invalid token']}, status=401)

  existing_user = User.objects.filter(email=claims['sub'])

  if not existing_user.exists():
    return JsonResponse({'errors': ['Invalid token']}, status=401)

  return JsonResponse({'email': existing_user.first().email}) 
