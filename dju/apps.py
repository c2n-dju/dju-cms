from django.apps import AppConfig


class DjuConfig(AppConfig):
    name = 'dju'
    verbose_name = "DJU CMS"

    def ready(self):
        import dju.signals.cas_saml #noqa
