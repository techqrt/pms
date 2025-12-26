from django.db import models
from django.db.models import Q
from pms_apps.authentication.models import User

class ArchiveLog(models.Model):

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

    log_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(
        User, verbose_name="User",
        on_delete=models.SET_NULL,
        null=True
    )
    ip_address = models.CharField(max_length=25)
    user_agent = models.TextField()
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model = models.CharField(max_length=20)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    end_point = models.CharField(max_length=125)
    details = models.JSONField()
    created_on = models.DateTimeField()

    class Meta:
        ordering = ['-created_on']
        db_table = "archive_log"

    def __str__(self) -> str:
            return f"{self.user.name} - {self.method}"

