from django.urls import path
from pms_apps.owner.controllers import OwnerViewController


urlpatterns = [
    path('create/', OwnerViewController.create_owner, name='create_owner'),
    path('update/', OwnerViewController.update_owner, name='update_owner'),
    path('delete/', OwnerViewController.delete_owner, name='delete_owner'),
    path('get/', OwnerViewController.get_owner, name='get_owner'),
    path('get_all/', OwnerViewController.get_all_owner,name='get_all_owner'),
]
