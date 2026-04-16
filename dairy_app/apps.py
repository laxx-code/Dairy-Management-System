from django.apps import AppConfig


class DairyAppConfig(AppConfig):
    name = 'dairy_app'

def ready(self):
    import dairy_app.signals