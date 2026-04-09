from django.db.models.signals import post_save, post_delete

EXCLUDE_FIELDS = ("created_at", "updated_at")


def capture_pre_update_data(sender, instance, include_fields=None, **kwargs):
    from pms_apps.activity_log.models.activity_log import ActivityLog
    from pms_apps.activity_log.models.archive_log import ArchiveLog
    from django.db.models import FileField

    if sender in (ActivityLog, ArchiveLog):
        return

    if not instance.pk:
        instance._old_data = None
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        instance._old_data = None
        return

    instance._old_data = {}
    for field in instance._meta.fields:
        if field.name not in EXCLUDE_FIELDS:
            if field.is_relation:
                value = getattr(old_instance, f"{field.name}_id")
            elif isinstance(field, FileField):
                # Convert FileField/ImageField objects to strings
                file_obj = getattr(old_instance, field.name)
                value = str(file_obj) if file_obj else None
            else:
                value = getattr(old_instance, field.name)
            instance._old_data[field.name] = value



def create_log_on_save_delete(
    sender,
    instance,
    created=False,
    signal=None,
    include_fields=None,
    **kwargs
):
    from pms_apps.activity_log.middlewares.log_middleware import local
    from pms_apps.activity_log.utils import ActivityLogUtils
    from pms_apps.activity_log.models.activity_log import ActivityLog
    from pms_apps.activity_log.models.archive_log import ArchiveLog
    from django.db.models import FileField

    if sender in (ActivityLog, ArchiveLog):
        return

    model_name = instance.__class__.__name__
    fields = instance._meta.fields
    details = {}

    if signal == post_save and not created:
        old_data = instance._old_data or {}
        fields = [f for f in fields if f.name not in EXCLUDE_FIELDS]

        changed_fields = []
        changed_old = {}
        changed_new = {}

        for field in fields:
            name = field.name

            old_val = old_data.get(name)
            
            if field.is_relation:
                new_val = getattr(instance, f"{name}_id")
            elif isinstance(field, FileField):
                # Convert FileField/ImageField objects to strings for JSON serialization
                file_obj = getattr(instance, name)
                new_val = str(file_obj) if file_obj else None
            else:
                new_val = getattr(instance, name)

            if old_val != new_val:
                changed_fields.append(name)
                changed_old[name] = old_val
                changed_new[name] = new_val

        if not changed_fields:
            return

        details = {
            "details": {
                "fields": changed_fields,
                "old": changed_old,
                "new": changed_new,
            }
        }

    else:
        snapshot = {}
        for field in instance._meta.fields:
            if not include_fields or field.name in include_fields:
                if field.is_relation:
                    value = getattr(instance, f"{field.name}_id")
                elif isinstance(field, FileField):
                    # Convert FileField/ImageField objects to strings for JSON serialization
                    file_obj = getattr(instance, field.name)
                    value = str(file_obj) if file_obj else None
                else:
                    value = getattr(instance, field.name)
                snapshot[field.name] = value

        details = {"snapshot": snapshot}

    ActivityLogUtils.create_activity_event(
        user_id=getattr(local, "user_id", ""),
        ip_address=getattr(local, "ip_address", ""),
        user_agent=getattr(local, "user_agent", ""),
        action="Delete" if signal == post_delete else "Create" if created else "Update",
        model=model_name,
        method=getattr(local, "method", ""),
        end_point=getattr(local, "end_point", ""),
        details=details,
    )
