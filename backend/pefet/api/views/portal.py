import json
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

import jwt
import qrcode

from ..models import Participant
from ..helpers import auth


@require_http_methods(['GET'])
def qr_code(request):
    try:
        claims = auth.extract_claims(
            request, secret=settings.PARTICIPANT_JWT_SECRET)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    try:
        participant = Participant.objects.get(id=claims['sub'])
    except:
        return JsonResponse({'errors': ['No such participant']}, status=404)

    qr_token = jwt.encode({'sub': participant.id, 'iat': datetime.timestamp(
        datetime.now())}, settings.QR_JWT_SECRET, algorithm='HS256')

    qr = qrcode.QRCode(
        version=15,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(qr_token)
    qr.make()
    img = qr.make_image()

    response = HttpResponse(content_type="image/png")
    img.save(response)

    return response
