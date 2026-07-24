from django.db import models
from django.db.models import Q
from pms_apps.authentication.models import User
from datetime import datetime
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from pms_apps.activity_log.models.archive_log import ArchiveLog
from django.core.exceptions import ValidationError

class ActivityLog(models.Model):

    ACTION_CHOICES = (
        ('Create','Create'),
        ('Update','Update'),
        ('Delete','Delete'),
    )

    METHOD_CHOICES = (
        ('POST','POST'),
        ('PUT','PUT'),
        ('PATCH','PATCH'),
        ('DELETE','DELETE')
    )

    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, verbose_name="User",
        on_delete=models.SET_NULL,
        null=True
    )
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField()
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model = models.CharField(max_length=50)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    end_point = models.CharField(max_length=125)
    details = models.JSONField(encoder=DjangoJSONEncoder)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        db_table = "activity_log"

    def __str__(self) -> str:
            return f"{self.user.phone_number if self.user else 'NA'} - {self.method}"
            

    @staticmethod
    def get_for_user(
        user_id : int,
        sort_by: str = "",
        sort_order: str = "",
        filter_key: str = "",
        filter_value: str = "",
        search_key: str = "",
     
    ) -> list:
        data = ActivityLog.objects.filter(user__user_id=user_id)

        if filter_key and filter_value:
            data = data.filter(**{filter_key: filter_value})

        if search_key:
            data = data.filter(
                Q(user__name__icontains=search_key) |
                Q(action__icontains=search_key) |
                Q(method__icontains=search_key) |
                Q(end_point__icontains=search_key) |
                Q(model__icontains=search_key)
            )

        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by
            )

        return list(
            data.values("log_id",
                        "ip_address","user_agent","action","model","method","end_point","details",
                        "created_on"
            )
        )


    @staticmethod
    def get_for_admin(
        sort_by: str = "",
        sort_order: str = "",
        filter_key: str = "",
        filter_value: str = "",
        search_key: str = "",
        from_date: datetime = None,
        to_date: datetime = None
    ) -> list:

        logs = ActivityLog.objects.values(
            "log_id", "user__user_id", "user__name", "user__phone_number", "user__email",
            "ip_address", "user_agent", "action", "model", "method", "end_point","details",
            "created_on"
        )

        archive_logs = ArchiveLog.objects.values(
            "log_id", "user__user_id", "user__name", "user__phone_number", "user__email",
            "ip_address", "user_agent", "action", "model", "method", "end_point","details",
            "created_on"
        )

        data = logs.union(archive_logs)

        if filter_key and filter_value:
            data = data.filter(**{filter_key: filter_value})

        if search_key:
            data = data.filter(
                Q(user__name__icontains=search_key) |
                Q(action__icontains=search_key) |
                Q(method__icontains=search_key) |
                Q(end_point__icontains=search_key) |
                Q(model__icontains=search_key)
            )

        if from_date or to_date:
            from_date = from_date or timezone.make_aware(datetime.min)
            to_date = to_date or timezone.make_aware(datetime.max)
            data = data.filter(created_on__range=(from_date, to_date))

        if sort_by:
            order = f"-{sort_by}" if sort_order == "desc" else sort_by
            data = data.order_by(order)

        return list(data)

