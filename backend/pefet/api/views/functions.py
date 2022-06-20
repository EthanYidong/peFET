import smtplib
from email.message import EmailMessage
from datetime import datetime, timezone
import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import Event, Participant
from ..helpers import auth, email


@require_http_methods(['POST'])
def send_emails(request, event_id):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'errors': ['No such event']}, status=404)

    if event.creator_id != claims['sub']:
        return JsonResponse({'errors': ['Unauthorized to run functions on this event']}, status=401)

    content = json.loads(request.body)

    to_email = []
    for participant_id in content['participants']:
        try:
            participant = Participant.objects.get(id=participant_id)
        except:
            pass
        if participant.event_id == event.id:
            to_email.append(participant)

    current_time = datetime.now(timezone.utc)

    server = smtplib.SMTP_SSL('smtp.sendgrid.net', 465)
    server.ehlo()
    server.login('apikey', settings.SENDGRID_API_KEY)

    for participant in to_email:
        msg = EmailMessage()
        msg['Subject'] = f'[peFET] {content["subject"]}'
        msg['From'] = 'peFET <pefet@blender.eu.org>'
        msg['To'] = f'{participant.name} <{participant.email}>'

        plain_content = email.PLAIN_TEMPLATE.substitute(
            name=participant.name,
            event_name=event.name,
            body=content['body'],
            portal_link=settings.FRONTEND_URL
        )
        html_content = email.HTML_TEMPLATE.substitute(
            name=participant.name,
            event_name=event.name,
            body=content['body'],
            portal_link=settings.FRONTEND_URL
        )
        msg.set_content(plain_content)
        msg.add_alternative(html_content, subtype="html")

        server.send_message(msg)

        participant.last_email_sent = current_time
        participant.save()

    server.quit()

    return JsonResponse({}, safe=False)
