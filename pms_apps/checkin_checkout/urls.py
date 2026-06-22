from django.urls import path
from pms_apps.checkin_checkout.controllers.check_in import CheckInViewController
from pms_apps.checkin_checkout.controllers.check_out import CheckOutViewController

urlpatterns = [
    path("check_in/create/", CheckInViewController.create, name="create_check_in"),
    path("check_in/get/", CheckInViewController.get, name="get_check_in"),
    path("check_in/get_all/", CheckInViewController.get_all, name="get_all_check_in"),
    path("check_in/delete/", CheckInViewController.delete, name="delete_check_in"),
    path("check_in/update/information/", CheckInViewController.update_information, name="update_check_in_information"),
    path("check_in/update/tenant_details/", CheckInViewController.update_tenant_details, name="update_check_in_tenant_details"),
    path("check_in/update/property_details/", CheckInViewController.update_property_details, name="update_check_in_property_details"),
    path("check_in/update/rental_details/", CheckInViewController.update_rental_details, name="update_check_in_rental_details"),
    path("check_in/update/property_inspection/", CheckInViewController.update_property_inspection, name="update_check_in_property_inspection"),
    path("check_in/update/repair_approval/", CheckInViewController.update_repair_approval, name="update_check_in_repair_approval"),
    path("check_in/update/utility_meter_readings/", CheckInViewController.update_utility_meter_readings, name="update_check_in_utility_meter_readings"),
    path("check_in/update/agreement_details/", CheckInViewController.update_agreement_details, name="update_check_in_agreement_details"),
    path("check_in/update/key_handover/", CheckInViewController.update_key_handover, name="update_check_in_key_handover"),
    path("check_in/update/comments/", CheckInViewController.update_comments, name="update_check_in_comments"),
    path("check_in/document/upload/", CheckInViewController.upload_document, name="upload_check_in_document"),
    path("check_in/inspection_item/create/", CheckInViewController.create_inspection_item, name="create_check_in_inspection_item"),
    path("check_in/inspection_item/update/", CheckInViewController.update_inspection_item, name="update_check_in_inspection_item"),
    path("check_in/inspection_item/delete/", CheckInViewController.delete_inspection_item, name="delete_check_in_inspection_item"),
    path("check_in/utility_reading/create/", CheckInViewController.create_utility_reading, name="create_check_in_utility_reading"),
    path("check_in/utility_reading/update/", CheckInViewController.update_utility_reading, name="update_check_in_utility_reading"),
    path("check_in/utility_reading/delete/", CheckInViewController.delete_utility_reading, name="delete_check_in_utility_reading"),
    path("check_in/payment/create/", CheckInViewController.create_payment, name="create_check_in_payment"),
    path("check_in/payment/update/", CheckInViewController.update_payment, name="update_check_in_payment"),
    path("check_in/payment/delete/", CheckInViewController.delete_payment, name="delete_check_in_payment"),
    path("check_in/key/create/", CheckInViewController.create_key, name="create_check_in_key"),
    path("check_in/key/update/", CheckInViewController.update_key, name="update_check_in_key"),
    path("check_in/key/delete/", CheckInViewController.delete_key, name="delete_check_in_key"),
]
