from django.apps import AppConfig
from pms_apps.activity_log.signals.log_signal import create_log_on_save_delete,capture_pre_update_data
from django.db.models.signals import post_save,post_delete,pre_save
from functools import partial

class ActivityLogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pms_apps.activity_log'

    def ready(self):
        from pms_apps.lead.models.lead import Lead
        from pms_apps.activity_log.utils import ActivityLogUtils

        utils = ActivityLogUtils()
        for model in [Lead]:
            included_fields = utils.get_log_include_fields(model._meta.model_name)
            post_save.connect(
                partial(
                    create_log_on_save_delete,
                    include_fields=included_fields
                ),
                sender=model,
                dispatch_uid="activity_log_lead_post_save")
            post_delete.connect(
                partial(
                    create_log_on_save_delete,
                    include_fields=included_fields
                ),
                sender=model,
                dispatch_uid="activity_log_lead_post_delete")
            pre_save.connect(
                partial(
                   capture_pre_update_data,
                   include_fields=included_fields 
                ),
                sender=model,
                dispatch_uid="activity_log_lead_pre_save"
            )