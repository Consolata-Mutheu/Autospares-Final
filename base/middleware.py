# middleware.py

from django.utils import timezone
from django.contrib.sessions.models import Session
from django.conf import settings

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the session key from the request
        session_key = request.session.session_key

        # Check if the user is authenticated and a session key exists
        if request.user.is_authenticated and session_key:
            # Get the session data from the database
            session_data = Session.objects.get(session_key=session_key).get_decoded()

            # Get the last activity time from the session data
            last_activity_str = session_data.get('last_activity')

            # Convert the last_activity string to a timezone-aware datetime object
            last_activity = timezone.datetime.strptime(last_activity_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc) if last_activity_str else None

            # Check if the session has timed out
            if last_activity and (timezone.now() - last_activity).seconds > settings.SESSION_COOKIE_AGE:
                # Log the user out if the session has timed out
                request.session.flush()

        response = self.get_response(request)

        # Update last activity time in the session data
        request.session['last_activity'] = timezone.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        return response
