from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response


class TimezoneTimeDetailAPIView(APIView):
    """
    Replace - with / in timezones.
    Because / character is used in most of the timezone names and conflicts with url /.

    e.g. Use Asia-Tehran rather than Asia/Tehran
    """

    def get(self, request, timezone):
        import pytz
        timezone = timezone.replace("-", "/")
        try:
            tz = pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            return Response({"detail": "Wrong timezone."}, status=400)
        now = datetime.now(tz)
        return Response({"now": now})
