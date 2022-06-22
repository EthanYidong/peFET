from django.http import JsonResponse

from jsonschema import validate, draft7_format_checker

import json


def json_data(schema=None):
    def inner(func):
        def wrapper(request, *args, **kwargs):
            try:
                data = json.loads(request.body)
            except:
                return JsonResponse({'errors': ['Invalid JSON']}, status=400)

            if schema:
                try:
                    validate(instance=data, schema=schema, format_checker=draft7_format_checker)
                except Exception as e:
                    return JsonResponse({'errors': [f'Invalid JSON: {e.message}']}, status=400)
            return func(request, *args, data=data, **kwargs)
        return wrapper
    return inner
