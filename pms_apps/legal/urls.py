from django.urls import path
from pms_apps.legal.controllers.legal_manager import LegalManagerViewController
from pms_apps.legal.controllers.legal_employee import LegalEmployeeViewController


urlpatterns = [
    path('manager/create/', LegalManagerViewController.create_manager, name='create_legal_manager'),
    path('manager/update/', LegalManagerViewController.update_manager, name='update_legal_manager'),
    path('manager/delete/', LegalManagerViewController.delete_manager, name='delete_legal_manager'),
    path('manager/get/', LegalManagerViewController.get_manager, name='get_legal_manager'),
    path('manager/get_all/', LegalManagerViewController.get_all_manager,name='get_all_legal_manager'),

    path('employee/create/', LegalEmployeeViewController.create_employee, name='create_legal_employee'),
    path('employee/update/', LegalEmployeeViewController.update_employee, name='update_legal_employee'),
    path('employee/delete/', LegalEmployeeViewController.delete_employee, name='delete_legal_employee'),
    path('employee/get/', LegalEmployeeViewController.get_employee, name='get_legal_employee'),
    path('employee/get_all/', LegalEmployeeViewController.get_all_employee,name='get_all_legal_employee'),
]
