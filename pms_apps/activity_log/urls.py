from django.urls import path
from pms_apps.activity_log.controller import ActivityLogController

urlpatterns = [
    path('logs/',ActivityLogController.get_for_user,name='log_get'),
    path('admin/logs/',ActivityLogController.get_for_admin,name='log_get_admin')
]