from django.apps import AppConfig


class CsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cs'

    def ready(self):
        import cs.signals