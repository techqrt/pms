from django.db import transaction
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
import json

from pms_apps.common.common import Common
from pms_apps.common.utils import Utils
from pms_apps.common.dataclasses.request.get_all import GetAll

from pms_apps.finance.models.finance_manager import FinanceManager
from pms_apps.finance.dataclasses.request.create.create_manager import FinanceManagerCreateRequest
from pms_apps.finance.dataclasses.request.update.update_manager import FinanceManagerUpdateRequest
from pms_apps.finance.serializers.response.get.get_manager import FinanceManagerResponseGetSerializer
from pms_apps.finance.serializers.response.get_all.get_all_manager import FinanceManagerResponseGetAllSerializer
from pms_apps.finance.utils import FinanceUtils


class FinanceManagerView:
    def __init__(self):
        self.manager_create = "Finance manager added successfully"
        self.manager_update = "Finance manager updated successfully"
        self.manager_delete = "Finance manager deleted successfully"

        self.data_no_match = "No matching record found"
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common().exception_handler
    def create_manager_extract(self, params: FinanceManagerCreateRequest):
        with transaction.atomic():
            obj = FinanceManager()
            manager_id = obj.create(
                manager_id=params.manager_id,
                name=params.name,
                dob=params.dob,
                department=params.department,
                total_budget_managed=params.total_budget_managed,
                reports_submitted=params.reports_submitted,
                team_size=params.team_size,
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(
                message=self.manager_create, data={"manager_id": manager_id})
        )

    @Common().exception_handler
    def update_manager_extract(self, params: FinanceManagerUpdateRequest):
        with transaction.atomic():
            if params.user_id != params.manager_id:
                raise ValueError("Not allowed to access this resource")
            manager_data = FinanceManager.get(manager_id=params.manager_id)
            if manager_data is None:
                raise ValueError(self.data_no_match)

            FinanceManager.update(
                manager_id=params.manager_id,
                name=params.name,
                dob=params.dob,
                department=params.department,
                total_budget_managed=params.total_budget_managed,
                reports_submitted=params.reports_submitted,
                team_size=params.team_size,
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.manager_update))

    @Common().exception_handler
    def delete_manager_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.manager_id:
                raise ValueError("Not allowed to access this resource")
            manager_data = FinanceManager.get(manager_id=params.manager_id)
            if manager_data is None:
                raise ValueError(self.data_no_match)
            FinanceManager.remove(manager_id=params.manager_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.manager_delete))

    @Common(response_handler=FinanceManagerResponseGetSerializer).exception_handler
    def get_manager_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.manager_id:
                raise ValueError("Not allowed to access this resource")
            manager_data = FinanceManager.get(manager_id=params.manager_id)
            if manager_data is None:
                raise ValueError(self.data_no_match)
            utils = FinanceUtils(entity='manager', columns_required=[
                column for column in params.values.split(',') if column])
            data = json.loads(utils.mapper([manager_data]))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common(response_handler=FinanceManagerResponseGetAllSerializer).exception_handler
    def get_all_manager_extract(self, params: GetAll):
        reversed_mapped = FinanceUtils.reverse_mapper([
            params.sort_by,
            params.filter_key
        ])

        pages = Paginator(FinanceManager.get_all(
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            filter_key=reversed_mapped.get(params.filter_key),
            filter_value=params.filter_value,
            search_key=params.search_key
        ), per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = pages.page(params.page_num)
        utils = FinanceUtils(entity='manager', columns_required=[
            column for column in params.values.split(',') if column])
        data = json.loads(utils.mapper(list(page_data)))

        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num, total_page=pages.num_pages,
                                        present_url=params.present_url,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
