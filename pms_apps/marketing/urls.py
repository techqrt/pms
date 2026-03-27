from django.urls import path
from pms_apps.marketing.controllers.marketing_manager import MarketingManagerViewController
from pms_apps.marketing.controllers.marketing_employee import MarketingEmployeeViewController
from pms_apps.marketing.controllers.marketing_comment import MarketingCommentViewController


urlpatterns = [
    path('manager/create/', MarketingManagerViewController.create_manager, name='create_marketing_manager'),
    path('manager/update/', MarketingManagerViewController.update_manager, name='update_marketing_manager'),
    path('manager/delete/', MarketingManagerViewController.delete_manager, name='delete_marketing_manager'),
    path('manager/get/', MarketingManagerViewController.get_manager, name='get_marketing_manager'),
    path('manager/get_all/', MarketingManagerViewController.get_all_manager,name='get_all_marketing_manager'),
    
    path('employee/create/', MarketingEmployeeViewController.create_employee, name='create_marketing_employee'),
    path('employee/update/', MarketingEmployeeViewController.update_employee, name='update_marketing_employee'),
    path('employee/delete/', MarketingEmployeeViewController.delete_employee, name='delete_marketing_employee'),
    path('employee/get/', MarketingEmployeeViewController.get_employee, name='get_marketing_employee'),
    path('employee/get_all/', MarketingEmployeeViewController.get_all_employee,name='get_all_marketing_employee'),
    
    path('comment/create/', MarketingCommentViewController.create_comment, name='create_marketing_comment'),
    path('comment/get_all/', MarketingCommentViewController.get_all_comments, name='get_all_marketing_comments'),
]
