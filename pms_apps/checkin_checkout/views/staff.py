from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from pms_apps.common.common import Common
from pms_apps.common.dataclasses.get_all import GetAll
from pms_apps.common.utils import Utils
from pms_apps.common.models.permissions import LeadPermission, PropertyPermission

from pms_apps.checkin_checkout.models.check_in_check_out_manager import CheckInCheckOutManager
from pms_apps.checkin_checkout.models.check_in_check_out_employee import CheckInCheckOutEmployee
from pms_apps.checkin_checkout.dataclasses.requests.update_manager import CheckInCheckOutManagerUpdateRequest
from pms_apps.checkin_checkout.dataclasses.requests.update_employee import CheckInCheckOutEmployeeUpdateRequest


class CheckInCheckOutStaffView:
    """Lists Check-In Check-Out Manager/Employee staff (id + name), the same
    role the Marketing manager/employee get_all endpoints play for the
    Marketing "Assigned Employee" dropdowns - so the equivalent Check-In/
    Check-Out dropdowns have a correct, department-scoped endpoint to call."""

    def __init__(self):
        self.data_get = "Data fetched successfully"
        self.data_update = "Updated successfully"
        self.data_no_match = "No matching record found"

    @staticmethod
    def _manager_row(row: dict) -> dict:
        return {
            "id": row["manager_id"],
            "name": row["name"],
            "role": "Manager",
            "phoneNumber": row.get("manager_id__phone_number"),
            "email": row.get("manager_id__email"),
        }

    @staticmethod
    def _employee_row(row: dict) -> dict:
        return {
            "id": row["employee_id"],
            "name": row["name"],
            "role": "Employee",
            "phoneNumber": row.get("employee_id__phone_number"),
            "email": row.get("employee_id__email"),
            "managerRefId": row.get("manager_ref_id"),
        }

    @Common().exception_handler
    def get_all_manager_extract(self, params: GetAll):
        manager_list = CheckInCheckOutManager.get_all(
            sort_by=params.sort_by,
            sort_order=params.sort_order,
            filter_key=params.filter_key,
            filter_value=params.filter_value,
            search_key=params.search_key,
        )

        pages = Paginator(manager_list, per_page=params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = [self._manager_row(row) for row in pages.page(params.page_num)]
        data = Utils.add_page_parameter(
            final_data=page_data, page_num=params.page_num, total_page=pages.num_pages,
            present_url=params.present_url,
            next_page_required=True if pages.num_pages != params.page_num else False,
        )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def get_all_employee_extract(self, params: GetAll):
        employee_list = CheckInCheckOutEmployee.get_all(
            sort_by=params.sort_by,
            sort_order=params.sort_order,
            filter_key=params.filter_key,
            filter_value=params.filter_value,
            search_key=params.search_key,
        )

        pages = Paginator(employee_list, per_page=params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = [self._employee_row(row) for row in pages.page(params.page_num)]
        data = Utils.add_page_parameter(
            final_data=page_data, page_num=params.page_num, total_page=pages.num_pages,
            present_url=params.present_url,
            next_page_required=True if pages.num_pages != params.page_num else False,
        )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def update_manager_extract(self, params: CheckInCheckOutManagerUpdateRequest):
        with transaction.atomic():
            if params.user_id != params.manager_id:
                raise ValueError("Not allowed to access this resource")
            manager_data = CheckInCheckOutManager.get(manager_id=params.manager_id)
            if manager_data is None:
                raise ValueError(self.data_no_match)

            lead_permission_id = None
            property_permission_id = None
            if params.permissions:
                if params.permissions.lead is not None:
                    lead_permission_id = manager_data.get('lead_permission__permission_id')
                    if lead_permission_id:
                        LeadPermission.update(permission_id=lead_permission_id, lead=params.permissions.lead)
                    else:
                        lead_permission_id = LeadPermission().create(lead=params.permissions.lead)
                if params.permissions.property is not None:
                    property_permission_id = manager_data.get('property_permission__permission_id')
                    if property_permission_id:
                        PropertyPermission.update(permission_id=property_permission_id, property=params.permissions.property)
                    else:
                        property_permission_id = PropertyPermission().create(property=params.permissions.property)

            CheckInCheckOutManager.update(
                manager_id=params.manager_id,
                name=params.name,
                dob=params.dob,
                department=params.department,
                team_size=params.team_size,
                lead_permission_id=lead_permission_id,
                property_permission_id=property_permission_id,
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    def update_employee_extract(self, params: CheckInCheckOutEmployeeUpdateRequest):
        with transaction.atomic():
            if params.user_id != params.employee_id:
                raise ValueError("Not allowed to access this resource")
            employee_data = CheckInCheckOutEmployee.get(employee_id=params.employee_id)
            if employee_data is None:
                raise ValueError(self.data_no_match)

            lead_permission_id = None
            property_permission_id = None
            if params.permissions:
                if params.permissions.lead is not None:
                    lead_permission_id = employee_data.get('lead_permission__permission_id')
                    if lead_permission_id:
                        LeadPermission.update(permission_id=lead_permission_id, lead=params.permissions.lead)
                    else:
                        lead_permission_id = LeadPermission().create(lead=params.permissions.lead)
                if params.permissions.property is not None:
                    property_permission_id = employee_data.get('property_permission__permission_id')
                    if property_permission_id:
                        PropertyPermission.update(permission_id=property_permission_id, property=params.permissions.property)
                    else:
                        property_permission_id = PropertyPermission().create(property=params.permissions.property)

            CheckInCheckOutEmployee.update(
                employee_id=params.employee_id,
                name=params.name,
                dob=params.dob,
                designation=params.designation,
                department=params.department,
                manager_ref=params.manager_ref,
                lead_permission_id=lead_permission_id,
                property_permission_id=property_permission_id,
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))
