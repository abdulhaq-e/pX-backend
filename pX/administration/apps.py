from django.apps import AppConfig


class AdministrationAppConfig(AppConfig):

    name = "pX.administration"
    label = "administration"
    verbose_name = "Administration"

    def ready(self):
        pass
        #connect_period_course_signals()
