from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import Event

import json

def all(request):
    data = list(Event.objects.values())
    return JsonResponse(data, safe=False)
    