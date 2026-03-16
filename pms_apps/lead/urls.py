from django.urls import path

from pms_apps.lead.controller import LeadViewController


urlpatterns = [
    path('create/',LeadViewController.create,name='lead_create'),
    path('update/',LeadViewController.update,name='lead_update'),
    path('delete/',LeadViewController.delete,name='lead_update'),
    path('get/',LeadViewController.get,name='lead_get'),
    path('get_all/',LeadViewController.get_all,name='lead_get_all'),
    path('count/',LeadViewController.count,name='lead_count')
]