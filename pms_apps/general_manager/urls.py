from django.urls import path
from pms_apps.general_manager.controllers import GeneralManagerViewController

urlpatterns = [
    path('create/', GeneralManagerViewController.create_general_manager, name='create_general_manager'),
    path('update/', GeneralManagerViewController.update_general_manager, name='update_general_manager'),
    path('delete/', GeneralManagerViewController.delete_general_manager, name='delete_general_manager'),
    path('get/', GeneralManagerViewController.get_general_manager, name='get_general_manager'),
    path('get_all/', GeneralManagerViewController.get_all_general_manager,name='get_all_general_manager'),
]
