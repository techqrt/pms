from django.db import transaction
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
import json

from pms_apps.common.common import Common
from pms_apps.common.utils import Utils
from pms_apps.common.dataclasses.request.get_all import GetAll
from pms_apps.authentication.models import User

from pms_apps.reception.models.reception_employee import ReceptionEmployee
from pms_apps.reception.dataclasses.request.create.create_employee import ReceptionEmployeeCreateRequest
from pms_apps.reception.dataclasses.request.update.update_employee import ReceptionEmployeeUpdateRequest
from pms_apps.reception.serializers.response.get.get_employee import ReceptionEmployeeResponseGetSerializer
from pms_apps.reception.serializers.response.get_all.get_all_employee import ReceptionEmployeeResponseGetAllSerializer

from pms_apps.reception.utils import ReceptionUtils


class ReceptionEmployeeView:
    def __init__(self):
        self.employee_create = "Reception employee added successfully"
        self.employee_update = "Reception employee updated successfully"
        self.employee_delete = "Reception employee deleted successfully"

        self.data_no_match = "No matching record found"
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common().exception_handler
    def create_employee_extract(self, params: ReceptionEmployeeCreateRequest):
        with transaction.atomic():
            _ = User.get(user_id=params.employee_id)

            obj = ReceptionEmployee()
            employee_id = obj.create(
                employee_id=params.employee_id,
                name=params.name,
                dob=params.dob,
                shift=params.shift,
                desk_number=params.desk_number,
                calls_handled=params.calls_handled,
                visitors_logged=params.visitors_logged,
                manager_ref=params.manager_ref,
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(
                message=self.employee_create, data={"employee_id": employee_id})
        )

    @Common().exception_handler
    def update_employee_extract(self, params: ReceptionEmployeeUpdateRequest):
        with transaction.atomic():
            if params.user_id != params.employee_id:
                raise ValueError("Not allowed to access this resource")
            employee_data = ReceptionEmployee.get(
                employee_id=params.employee_id)
            if employee_data is None:
                raise ValueError(self.data_no_match)

            ReceptionEmployee.update(
                employee_id=params.employee_id,
                name=params.name,
                dob=params.dob,
                shift=params.shift,
                desk_number=params.desk_number,
                calls_handled=params.calls_handled,
                visitors_logged=params.visitors_logged,
                manager_ref=params.manager_ref,
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.employee_update))

    @Common().exception_handler
    def delete_employee_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.employee_id:
                raise ValueError("Not allowed to access this resource")
            employee_data = ReceptionEmployee.get(
                employee_id=params.employee_id)
            if employee_data is None:
                raise ValueError(self.data_no_match)
            ReceptionEmployee.remove(employee_id=params.employee_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.employee_delete))

    @Common(response_handler=ReceptionEmployeeResponseGetSerializer).exception_handler
    def get_employee_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.employee_id:
                raise ValueError("Not allowed to access this resource")
            employee_data = ReceptionEmployee.get(
                employee_id=params.employee_id)
            if employee_data is None:
                raise ValueError(self.data_no_match)
            utils = ReceptionUtils(entity='employee', columns_required=[
                column for column in params.values.split(',') if column])
            data = json.loads(utils.mapper([employee_data]))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common(response_handler=ReceptionEmployeeResponseGetAllSerializer).exception_handler
    def get_all_employee_extract(self, params: GetAll):
        reversed_mapped = ReceptionUtils.reverse_mapper([
            params.sort_by,
            params.filter_key
        ])

        sort_by_db = reversed_mapped.get(params.sort_by) or params.sort_by
        filter_key_db = reversed_mapped.get(
            params.filter_key) or params.filter_key

        pages = Paginator(ReceptionEmployee.get_all(
            sort_by=sort_by_db,
            sort_order=params.sort_order,
            filter_key=filter_key_db,
            filter_value=params.filter_value,
            search_key=params.search_key
        ), per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = pages.page(params.page_num)
        utils = ReceptionUtils(entity='employee', columns_required=[
            column for column in params.values.split(',') if column])
        data = json.loads(utils.mapper(list(page_data)))

        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num, total_page=pages.num_pages,
                                        present_url=params.present_url,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
