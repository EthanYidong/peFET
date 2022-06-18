from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

import json

from ..models import Event
from ..helpers import auth


@require_http_methods(['GET'])
def all(request):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    data = list(Event.objects.filter(creator_id=claims['sub']).values())
    return JsonResponse(data, safe=False)


@require_http_methods(['POST'])
def create(request):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    content = json.loads(request.body)

    event_date = datetime.strptime(content['date'], '%Y-%m-%d').date()

    new_event = Event(name=content["name"],
                      date=event_date, creator_id=claims['sub'])
    new_event.save()

    return JsonResponse({"id": new_event.id})
