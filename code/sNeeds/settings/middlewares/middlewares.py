import pytz

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.META.get("HTTP_CLIENT_TIMEZONE")
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()

        return self.get_response(request)

class CORSMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import json
        print("request: ")
        print(json.dumps(dict(request.headers), indent=4, sort_keys=True))
        print("------------------------ ")

        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"

        print("response: ")
        print(json.dumps(dict(response.headers), indent=4, sort_keys=True))
        return response