from django.http import HttpResponse
from django.http import JsonResponse
from .models import User
from .models import Event
from .models import Participant
from django.shortcuts import render
import json

# Create your views here.

# hello world test
def index(request):
    return HttpResponse("This is the api index page.")


def json(request):
    data = list(Event.objects.values())
    return JsonResponse(data, safe=False)
    