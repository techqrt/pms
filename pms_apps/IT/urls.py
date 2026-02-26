from django.urls import path
from pms_apps.IT.controllers.IT_manager import ITManagerViewController
from pms_apps.IT.controllers.IT_employee import ITEmployeeViewController
from pms_apps.IT.controllers.IT_technician import ITTechnicianViewController


urlpatterns = [
    path('manager/create/', ITManagerViewController.create_manager, name='create_IT_manager'),
    path('manager/update/', ITManagerViewController.update_manager, name='update_IT_manager'),
    path('manager/delete/', ITManagerViewController.delete_manager, name='delete_IT_manager'),
    path('manager/get/', ITManagerViewController.get_manager, name='get_IT_manager'),
    path('manager/get_all/', ITManagerViewController.get_all_manager,name='get_all_IT_manager'),

    path('employee/create/', ITEmployeeViewController.create_employee, name='create_IT_employee'),
    path('employee/update/', ITEmployeeViewController.update_employee, name='update_IT_employee'),
    path('employee/delete/', ITEmployeeViewController.delete_employee, name='delete_IT_employee'),
    path('employee/get/', ITEmployeeViewController.get_employee, name='get_IT_employee'),
    path('employee/get_all/', ITEmployeeViewController.get_all_employee,name='get_all_IT_employee'),

    path('technician/create/', ITTechnicianViewController.create_technician, name='create_IT_technician'),
    path('technician/update/', ITTechnicianViewController.update_technician, name='update_IT_technician'),
    path('technician/delete/', ITTechnicianViewController.delete_technician, name='delete_IT_technician'),
    path('technician/get/', ITTechnicianViewController.get_technician, name='get_IT_technician'),
    path('technician/get_all/', ITTechnicianViewController.get_all_technician,name='get_all_IT_technician'),
]
