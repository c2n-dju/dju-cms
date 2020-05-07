from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from re import compile

EXEMPT_URLS = [compile('^(|fr/|en/)login'),
               compile('^(|fr/|en/)logout'),
               compile('^(|fr/|en/)admin'),
]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

# print('EXEMPT_URLS = ' + str(EXEMPT_URLS))
    
class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), (
            'The LoginRequiredMiddleware requires authentication middleware '
            'to be installed. Edit your MIDDLEWARE setting to insert before '
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        path = request.path
        if request.user.is_authenticated:
            return
        return HttpResponseRedirect(settings.LOGIN_URL)
