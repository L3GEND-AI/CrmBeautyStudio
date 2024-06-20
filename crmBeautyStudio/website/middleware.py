import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        if 'last_activity' in request.session:
            last_activity = datetime.datetime.strptime(request.session['last_activity'], '%Y-%m-%d %H:%M:%S.%f')
            now = datetime.datetime.now()
            if (now - last_activity).seconds > settings.SESSION_COOKIE_AGE:
                logout(request)
                return
        request.session['last_activity'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
