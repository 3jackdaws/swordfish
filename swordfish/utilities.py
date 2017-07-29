import json
from django.http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, content={}, *args, **kwargs):
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(json.dumps(content, indent=2), *args, **kwargs)
