from django.apps import AppConfig

class UISConfig(AppConfig):
    name = 'UIS'

    def ready(self):
        import UIS.signals
