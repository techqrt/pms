from django.db import transaction
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
import json

from pms_apps.common.common import Common
from pms_apps.common.utils import Utils
from pms_apps.common.dataclasses.request.get_all import GetAll
from pms_apps.authentication.models import User

from pms_apps.marketing.models.marketing_employee import MarketingEmployee
from pms_apps.marketing.models.marketing_permission import MarketingPermission
from pms_apps.marketing.dataclasses.request.create.create_employee import MarketingEmployeeCreateRequest
from pms_apps.marketing.dataclasses.request.update.update_employee import MarketingEmployeeUpdateRequest
from pms_apps.marketing.serializers.response.get.get_employee import MarketingEmployeeResponseGetSerializer
from pms_apps.marketing.serializers.response.get_all.get_all_employee import MarketingEmployeeResponseGetAllSerializer

from pms_apps.marketing.utils import MarketingUtils


class MarketingEmployeeView:
    def __init__(self):
        self.employee_create = "Marketing employee added successfully"
        self.employee_update = "Marketing employee updated successfully"
        self.employee_delete = "Marketing employee deleted successfully"

        self.data_no_match = "No matching record found"
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common().exception_handler
    def create_employee_extract(self, params: MarketingEmployeeCreateRequest):
        with transaction.atomic():
            _ = User.get(user_id=params.employee_id)

            permission_id = None
            if hasattr(params, 'permission') and params.permission:
                permission_obj = MarketingPermission()
                permission_id = permission_obj.create(
                    lead=params.permission.lead,
                    property=params.permission.property
                )

            obj = MarketingEmployee()
            employee_id = obj.create(
                employee_id=params.employee_id,
                name=params.name,
                dob=params.dob,
                designation=params.designation,
                department=params.department,
                campaigns_assigned=params.campaigns_assigned,
                leads_generated=params.leads_generated,
                manager_ref=params.manager_ref,
                permission_id=permission_id,
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(
                message=self.employee_create, data={"employee_id": employee_id})
        )

    @Common().exception_handler
    def update_employee_extract(self, params: MarketingEmployeeUpdateRequest):
        with transaction.atomic():
            employee_data = MarketingEmployee.get(
                employee_id=params.employee_id)
            if employee_data is None:
                raise ValueError(self.data_no_match)

            permission_id = employee_data.get('permission_id')
            if hasattr(params, 'permission') and params.permission:
                if permission_id:
                    MarketingPermission.update(
                        permission_id=permission_id,
                        lead=params.permission.lead,
                        property=params.permission.property
                    )
                else:
                    permission_obj = MarketingPermission()
                    permission_id = permission_obj.create(
                        lead=params.permission.lead,
                        property=params.permission.property
                    )

            MarketingEmployee.update(
                employee_id=params.employee_id,
                name=params.name,
                dob=params.dob,
                designation=params.designation,
                department=params.department,
                campaigns_assigned=params.campaigns_assigned,
                leads_generated=params.leads_generated,
                manager_ref=params.manager_ref,
                permission_id=permission_id,
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.employee_update))

    @Common().exception_handler
    def delete_employee_extract(self, params):
        with transaction.atomic():
            employee_data = MarketingEmployee.get(
                employee_id=params.employee_id)
            if employee_data is None:
                raise ValueError(self.data_no_match)
            MarketingEmployee.remove(employee_id=params.employee_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.employee_delete))

    @Common(response_handler=MarketingEmployeeResponseGetSerializer).exception_handler
    def get_employee_extract(self, params):
        with transaction.atomic():
            employee_data = MarketingEmployee.get(
                employee_id=params.employee_id)
            if employee_data is None:
                raise ValueError(self.data_no_match)
            utils = MarketingUtils(entity='employee', columns_required=[
                                   column for column in params.values.split(',') if column])
            data = json.loads(utils.mapper([employee_data]))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common(response_handler=MarketingEmployeeResponseGetAllSerializer).exception_handler
    def get_all_employee_extract(self, params: GetAll):
        reversed_mapped = MarketingUtils.reverse_mapper([
            params.sort_by,
            params.filter_key
        ])

        sort_by_db = reversed_mapped.get(params.sort_by) or params.sort_by
        filter_key_db = reversed_mapped.get(
            params.filter_key) or params.filter_key

        pages = Paginator(MarketingEmployee.get_all(
            sort_by=sort_by_db,
            sort_order=params.sort_order,
            filter_key=filter_key_db,
            filter_value=params.filter_value,
            search_key=params.search_key
        ), per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = pages.page(params.page_num)
        utils = MarketingUtils(entity='employee', columns_required=[
                               column for column in params.values.split(',') if column])
        data = json.loads(utils.mapper(list(page_data)))

        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num, total_page=pages.num_pages,
                                        present_url=params.present_url,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
