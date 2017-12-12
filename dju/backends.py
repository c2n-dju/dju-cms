from django_cas_ng.backends import CASBackend
from django.contrib import messages
from django.conf import settings


class DjuCASBackend(CASBackend):
    def user_can_authenticate(self, user):
        return True

    def bad_attributes_reject(self, request, username, attributes):
        attribute = settings.C2N_SAML_CONTROL[0]
        value = settings.C2N_SAML_CONTROL[1]

        if attribute not in attributes:
            message = 'No \''+ attribute + '\' in SAML attributes'
            messages.add_message(request, messages.ERROR, message)
            return message

        if value not in attributes[attribute]:
            message = 'User ' + str(username) + ' is not in ' + value + ' ' + attribute + ', should be one of ' + str(attributes[attribute])
            messages.add_message(request, messages.ERROR, message)
            print('Faute de Sentry, voici le message: ' + message)
            return message
            
        return None
