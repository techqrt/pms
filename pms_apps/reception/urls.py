from django.urls import path
from pms_apps.reception.controllers.reception_manager import ReceptionManagerViewController
from pms_apps.reception.controllers.reception_employee import ReceptionEmployeeViewController


urlpatterns = [
    path('manager/create/', ReceptionManagerViewController.create_manager, name='create_reception_manager'),
    path('manager/update/', ReceptionManagerViewController.update_manager, name='update_reception_manager'),
    path('manager/delete/', ReceptionManagerViewController.delete_manager, name='delete_reception_manager'),
    path('manager/get/', ReceptionManagerViewController.get_manager, name='get_reception_manager'),
    path('manager/get_all/', ReceptionManagerViewController.get_all_manager,name='get_all_reception_manager'),

    path('employee/create/', ReceptionEmployeeViewController.create_employee, name='create_reception_employee'),
    path('employee/update/', ReceptionEmployeeViewController.update_employee, name='update_reception_employee'),
    path('employee/delete/', ReceptionEmployeeViewController.delete_employee, name='delete_reception_employee'),
    path('employee/get/', ReceptionEmployeeViewController.get_employee, name='get_reception_employee'),
    path('employee/get_all/', ReceptionEmployeeViewController.get_all_employee,name='get_all_reception_employee'),
]
