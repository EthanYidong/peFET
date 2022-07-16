from ast import Bytes
from datetime import datetime
from functools import partial
from io import BytesIO
import uuid

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict

import jwt
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode as decodeQr

from ..models import Participant, UploadedFetImage
from ..helpers import auth
from ..cv import detect


@require_http_methods(['GET'])
def me(request):
    try:
        claims = auth.extract_claims(
            request, secret=settings.PARTICIPANT_JWT_SECRET)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    try:
        participant = Participant.objects.get(id=claims['sub'])
    except:
        return JsonResponse({'errors': ['No such participant']}, status=404)

    return JsonResponse({'participant': model_to_dict(participant)}, safe=False)

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

    response = HttpResponse(content_type='image/png')
    img.save(response)

    return response


@require_http_methods(['POST'])
def upload_image(request):
    try:
        claims = auth.extract_claims(
            request, secret=settings.PARTICIPANT_JWT_SECRET)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    try:
        participant = Participant.objects.get(id=claims['sub'])
    except:
        return JsonResponse({'errors': ['No such participant']}, status=404)

    uploaded_file = request.FILES['image']

    if uploaded_file.size >= 1024 * 1024 * 16:
        return JsonResponse({'errors': ['Image is too large']}, status=413)

    image_buf = bytearray([])
    for chunk in uploaded_file.chunks():
        image_buf.extend(chunk)

    image = Image.open(BytesIO(image_buf))

    qr_data = decodeQr(image)
    detected_image = detect.extractTestImg(image)

    resize_ratio = max(image.width, image.height) / settings.MAX_IMAGE_DIMS
    if resize_ratio > 1:
        image = image.resize(
            (int(image.width // resize_ratio), int(image.height // resize_ratio)))

    partial_path = f'uploads/fet/{uuid.uuid4()}.png'
    full_path = settings.MEDIA_ROOT / partial_path
    image.save(full_path, 'PNG')

    detected_partial_path = None
    if detected_image is not None:
        detected_partial_path = f'uploads/fet/{uuid.uuid4()}.png'
        detected_full_path = settings.MEDIA_ROOT / detected_partial_path
        detected_image.save(detected_full_path, 'PNG')


    new_upload = UploadedFetImage(
        participant_id=participant.id, original_image=partial_path, extracted_image=detected_partial_path)
    new_upload.save()

    if not qr_data:
        return JsonResponse({'errors': ['QR code was not found in image']}, status=400)

    for qr in qr_data:
        try:
            claims = jwt.decode(qr.data, settings.QR_JWT_SECRET, ['HS256'])
            passed = datetime.now() - datetime.fromtimestamp(claims['iat'])

            if passed.total_seconds() < settings.MAX_QR_AGE:
                participant.status = Participant.SUBMITTED
                participant.save()
                return JsonResponse({})
            else:
                return JsonResponse({'errors': ['QR code was too old']}, status=400)
        except jwt.PyJWTError:
            pass

    return JsonResponse({'errors': ['QR code was invalid']}, status=400)
