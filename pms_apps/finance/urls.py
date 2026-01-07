from django.urls import path
from pms_apps.finance.controllers.finance_manager import FinanceManagerViewController
from pms_apps.finance.controllers.finance_employee import FinanceEmployeeViewController


urlpatterns = [
    path('manager/create/', FinanceManagerViewController.create_manager, name='create_finance_manager'),
    path('manager/update/', FinanceManagerViewController.update_manager, name='update_finance_manager'),
    path('manager/delete/', FinanceManagerViewController.delete_manager, name='delete_finance_manager'),
    path('manager/get/', FinanceManagerViewController.get_manager, name='get_finance_manager'),
    path('manager/get_all/', FinanceManagerViewController.get_all_manager,name='get_all_finance_manager'),

    path('employee/create/', FinanceEmployeeViewController.create_employee, name='create_finance_employee'),
    path('employee/update/', FinanceEmployeeViewController.update_employee, name='update_finance_employee'),
    path('employee/delete/', FinanceEmployeeViewController.delete_employee, name='delete_finance_employee'),
    path('employee/get/', FinanceEmployeeViewController.get_employee, name='get_finance_employee'),
    path('employee/get_all/', FinanceEmployeeViewController.get_all_employee,name='get_all_finance_employee'),
]
