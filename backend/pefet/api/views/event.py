from datetime import date
import json
import csv

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from email_validator import validate_email

from ..models import Event, Participant
from ..helpers import auth, json_data


@require_http_methods(['GET'])
def all(request):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    data = list(Event.objects.filter(creator_id=claims['sub']).values())
    return JsonResponse({'events': data}, safe=False)


@require_http_methods(['POST'])
@json_data(schema={
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'date': {'type': 'string', 'format': 'date'},
    },
    'required': ['name', 'date']
})
def create(request, data):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    try:
        event_date = date.fromisoformat(data['date'])
    except:
        return JsonResponse({'errors': ['Invalid date']}, status=401)

    new_event = Event(name=data['name'],
                      date=event_date, creator_id=claims['sub'])
    new_event.save()

    return JsonResponse({'id': new_event.id})


@require_http_methods(['POST'])
@require_http_methods(['POST'])
@json_data(schema={
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'date': {'type': 'string', 'format': 'date'},
    },
    'required': ['name', 'date']
})
def update(request, event_id, data):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    try:
        existing_event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'errors': ['No such event']}, status=404)

    if existing_event.creator_id != claims['sub']:
        return JsonResponse({'errors': ['Unauthorized to update this event']}, status=401)

    existing_event.name = data['name']
    existing_event.date = date.fromisoformat(data['date'])
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
@json_data(schema={
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
    },
    'required': ['name', 'email']
})
def create_participant(request, event_id, data):
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

    try:
        email = validate_email(data['email'], check_deliverability=False).email
    except:
        return JsonResponse({'errors': ['Invalid email format']}, status=400)

    if Participant.objects.filter(event_id=event.id, email=email).count() != 0:
        return JsonResponse({'errors': ['Participant with that email already exists']}, status=400)

    new_participant = Participant(
        name=data['name'], email=email, event_id=event.id)
    new_participant.save()

    return JsonResponse({'id': new_participant.id}, safe=False)


@require_http_methods(['POST'])
def create_participants_csv(request, event_id):
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

    uploaded_file = request.FILES['csv']

    if uploaded_file.size >= 1024 * 1024 * 16:
        return JsonResponse({'errors': ['Data is too large']}, status=413)

    file_buf = bytearray([])
    for chunk in uploaded_file.chunks():
        file_buf.extend(chunk)

    file_data = file_buf.decode('utf-8').splitlines()

    data_reader = csv.reader(file_data)

    errors = []

    for row in data_reader:
        name = row[0]
        email = row[1]

        valid = True

        if not name or not email:
            continue

        try:
            email = validate_email(email, check_deliverability=False).email
        except:
            valid = False
            errors.append(f'[{email}] Invalid email format')

        if Participant.objects.filter(event_id=event.id, email=email).count() != 0:
            valid = False
            errors.append(f'[{email}] Participant with that email already exists')

        if valid:
            new_participant = Participant(
                name=name, email=email, event_id=event.id)
            new_participant.save()

    status = 200 if not errors else 400

    return JsonResponse({ 'errors': errors }, status=status)


@require_http_methods(['POST'])
@json_data(schema={
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
    },
    'required': ['name', 'email']
})
def update_participant(request, event_id, participant_id, data):
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

    try:
        existing_participant = Participant.objects.get(id=participant_id)
    except:
        return JsonResponse({'errors': ['Participant does not exist']}, status=404)

    if existing_participant.event_id != event.id:
        return JsonResponse({'errors': ['Participant does not belong to this event']}, status=400)

    try:
        email = validate_email(data['email'], check_deliverability=False).email
    except:
        return JsonResponse({'errors': ['Invalid email format']}, status=400)

    if Participant.objects.filter(event_id=event.id, email=email).count() != 0:
        return JsonResponse({'errors': ['Participant with that email already exists']}, status=400)


    existing_participant.name = data['name']
    existing_participant.email = data['email']
    existing_participant.save()

    return JsonResponse({})
