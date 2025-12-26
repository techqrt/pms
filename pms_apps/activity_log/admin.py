from django.contrib import admin
from pms_apps.activity_log.models.activity_log import ActivityLog
from pms_apps.activity_log.models.archive_log import ArchiveLog

admin.site.register(ActivityLog)
admin.site.register(ArchiveLog)