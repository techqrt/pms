from django.urls import path
from pms_apps.collection.controllers.collection_manager import CollectionManagerViewController
from pms_apps.collection.controllers.collection_employee import CollectionEmployeeViewController


urlpatterns = [
    path('manager/create/', CollectionManagerViewController.create_manager, name='create_collection_manager'),
    path('manager/update/', CollectionManagerViewController.update_manager, name='update_collection_manager'),
    path('manager/delete/', CollectionManagerViewController.delete_manager, name='delete_collection_manager'),
    path('manager/get/', CollectionManagerViewController.get_manager, name='get_collection_manager'),
    path('manager/get_all/', CollectionManagerViewController.get_all_manager,name='get_all_collection_manager'),

    path('employee/create/', CollectionEmployeeViewController.create_employee, name='create_collection_employee'),
    path('employee/update/', CollectionEmployeeViewController.update_employee, name='update_collection_employee'),
    path('employee/delete/', CollectionEmployeeViewController.delete_employee, name='delete_collection_employee'),
    path('employee/get/', CollectionEmployeeViewController.get_employee, name='get_collection_employee'),
    path('employee/get_all/', CollectionEmployeeViewController.get_all_employee,name='get_all_collection_employee'),
]
