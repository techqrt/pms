from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pms_apps.common'

    # def ready(self):
    #     from biller_apps.common.signals import Signals
    #     Signals()
