from datetime import datetime
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import Event, Participant
from ..helpers import auth


@require_http_methods(['GET'])
def all(request):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    data = list(Event.objects.filter(creator_id=claims['sub']).values())
    return JsonResponse({'events': data}, safe=False)


@require_http_methods(['POST'])
def create(request):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    content = json.loads(request.body)

    event_date = datetime.strptime(content['date'], '%Y-%m-%d').date()

    new_event = Event(name=content['name'],
                      date=event_date, creator_id=claims['sub'])
    new_event.save()

    return JsonResponse({'id': new_event.id})


@require_http_methods(['POST'])
def update(request, event_id):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    content = json.loads(request.body)

    try:
        existing_event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'errors': ['No such event']}, status=404)

    if existing_event.creator_id != claims['sub']:
        return JsonResponse({'errors': ['Unauthorized to update this event']}, status=401)

    existing_event.name = content['name']
    existing_event.date = datetime.strptime(content['date'], '%Y-%m-%d').date()
    existing_event.save()

    return JsonResponse({})


@require_http_methods(['GET'])
def read_participants(request, event_id):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'errors': ['No such event']}, status=404)

    if event.creator_id != claims['sub']:
        return JsonResponse({'errors': ['Unauthorized to read from this event']}, status=401)

    data = list(Participant.objects.filter(event_id=event.id).values())
    return JsonResponse({'participants': data}, safe=False)


@require_http_methods(['POST'])
def create_participant(request, event_id):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'errors': ['No such event']}, status=404)

    if event.creator_id != claims['sub']:
        return JsonResponse({'errors': ['Unauthorized to update this event']}, status=401)

    content = json.loads(request.body)

    new_participant = Participant(
        name=content['name'], email=content['email'], event_id=event.id)
    new_participant.save()

    return JsonResponse({'id': new_participant.id}, safe=False)


@require_http_methods(['POST'])
def update_participant(request, event_id):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'errors': ['No such event']}, status=404)

    if event.creator_id != claims['sub']:
        return JsonResponse({'errors': ['Unauthorized to update this event']}, status=401)

    content = json.loads(request.body)

    try:
        existing_participant = Participant.objects.get(id=content['id'])
    except:
        return JsonResponse({'errors': ['Participant does not exist']}, status=404)

    if existing_participant.event_id != event.id:
        return JsonResponse({'errors': ['Participant does not belong to this event']}, status=400)

    existing_participant.name = content['name']
    existing_participant.email = content['email']
    existing_participant.save()

    return JsonResponse({})
