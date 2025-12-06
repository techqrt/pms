from django.urls import path
from pms_apps.maintenance.controllers.maintenance_manager import MaintenanceManagerViewController
from pms_apps.maintenance.controllers.maintenance_employee import MaintenanceEmployeeViewController
from pms_apps.maintenance.controllers.maintenance_technician import MaintenanceTechnicianViewController


urlpatterns = [
    path('manager/create/', MaintenanceManagerViewController.create_manager, name='create_maintenance_manager'),
    path('manager/update/', MaintenanceManagerViewController.update_manager, name='update_maintenance_manager'),
    path('manager/delete/', MaintenanceManagerViewController.delete_manager, name='delete_maintenance_manager'),
    path('manager/get/', MaintenanceManagerViewController.get_manager, name='get_maintenance_manager'),
    path('manager/get_all/', MaintenanceManagerViewController.get_all_manager,name='get_all_maintenance_manager'),

    path('employee/create/', MaintenanceEmployeeViewController.create_employee, name='create_maintenance_employee'),
    path('employee/update/', MaintenanceEmployeeViewController.update_employee, name='update_maintenance_employee'),
    path('employee/delete/', MaintenanceEmployeeViewController.delete_employee, name='delete_maintenance_employee'),
    path('employee/get/', MaintenanceEmployeeViewController.get_employee, name='get_maintenance_employee'),
    path('employee/get_all/', MaintenanceEmployeeViewController.get_all_employee,name='get_all_maintenance_employee'),

    path('technician/create/', MaintenanceTechnicianViewController.create_technician, name='create_maintenance_technician'),
    path('technician/update/', MaintenanceTechnicianViewController.update_technician, name='update_maintenance_technician'),
    path('technician/delete/', MaintenanceTechnicianViewController.delete_technician, name='delete_maintenance_technician'),
    path('technician/get/', MaintenanceTechnicianViewController.get_technician, name='get_maintenance_technician'),
    path('technician/get_all/', MaintenanceTechnicianViewController.get_all_technician,name='get_all_maintenance_technician'),
]
