from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import Event
from ..helpers import auth

def all(request):
    try:
        claims = auth.extract_claims(request)
    except:
        return JsonResponse({'errors': ['Invalid token']}, status=401)

    data = list(Event.objects.filter(creator_id = claims['sub']).values())
    return JsonResponse(data, safe=False)
