from django.conf import settings

import re
import jwt


class TokenMissingError(Exception):
    """Token was not present in request"""
    pass


class InvalidTokenError(Exception):
    """Token was present but invalid"""
    pass


def extract_claims(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if auth_header is None:
        raise TokenMissingError

    try:
        token = re.match("^Bearer ([\S]+)$", auth_header).group(1)
    except:
        raise TokenMissingError

    try:
        claims = jwt.decode(token, settings.JWT_SECRET, ['HS256'])
    except:
        raise InvalidTokenError

    return claims
