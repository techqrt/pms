from django.db import transaction
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
import json

from pms_apps.common.common import Common
from pms_apps.common.utils import Utils
from pms_apps.common.dataclasses.request.get_all import GetAll

from pms_apps.general_manager.models import GeneralManager
from pms_apps.general_manager.dataclasses.request.create import GeneralManagerCreateRequest
from pms_apps.general_manager.dataclasses.request.update import GeneralManagerUpdateRequest
from pms_apps.general_manager.serializers.response.get import GeneralManagerResponseGetSerializer
from pms_apps.general_manager.serializers.response.get_all import GeneralManagerResponseGetAllSerializer
from pms_apps.general_manager.utils import GeneralManagerUtils


class GeneralManagerView:
    def __init__(self):
        self.general_manager_create = "General Manager added successfully"
        self.general_manager_update = "General Manager updated successfully"
        self.general_manager_delete = "General Manager deleted successfully"

        self.data_no_match = "No matching record found"
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common().exception_handler
    def create_general_manager_extract(self, params: GeneralManagerCreateRequest):
        with transaction.atomic():
            obj = GeneralManager()
            general_manager_id = obj.create(
                general_manager_id=params.general_manager_id,
                name=params.name,
                dob=params.dob,
                department=params.department,
                years_of_experience=params.years_of_experience,
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(
                message=self.general_manager_create, data={"general_manager_id": general_manager_id})
        )

    @Common().exception_handler
    def update_general_manager_extract(self, params: GeneralManagerUpdateRequest):
        with transaction.atomic():
            if params.user_id != params.general_manager_id:
                raise ValueError("Not allowed to access this resource")
            general_manager_data = GeneralManager.get(general_manager_id=params.general_manager_id)
            if general_manager_data is None:
                raise ValueError(self.data_no_match)

            GeneralManager.update(
                general_manager_id=params.general_manager_id,
                name=params.name,
                dob=params.dob,
                department=params.department,
                years_of_experience=params.years_of_experience,
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.general_manager_update))

    @Common().exception_handler
    def delete_general_manager_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.general_manager_id:
                raise ValueError("Not allowed to access this resource")
            general_manager_data = GeneralManager.get(general_manager_id=params.general_manager_id)
            if general_manager_data is None:
                raise ValueError(self.data_no_match)
            GeneralManager.remove(general_manager_id=params.general_manager_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.general_manager_delete))

    @Common(response_handler=GeneralManagerResponseGetSerializer).exception_handler
    def get_general_manager_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.general_manager_id:
                raise ValueError("Not allowed to access this resource")
            general_manager_data = GeneralManager.get(general_manager_id=params.general_manager_id)
            if general_manager_data is None:
                raise ValueError(self.data_no_match)
            utils = GeneralManagerUtils(entity='general_manager', columns_required=[
                column for column in params.values.split(',') if column])
            data = json.loads(utils.mapper([general_manager_data]))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common(response_handler=GeneralManagerResponseGetAllSerializer).exception_handler
    def get_all_general_manager_extract(self, params: GetAll):
        reversed_mapped = GeneralManagerUtils.reverse_mapper([
            params.sort_by,
            params.filter_key
        ])

        pages = Paginator(GeneralManager.get_all(
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            filter_key=reversed_mapped.get(params.filter_key),
            filter_value=params.filter_value,
            search_key=params.search_key
        ), per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = pages.page(params.page_num)
        utils = GeneralManagerUtils(entity='general_manager', columns_required=[
            column for column in params.values.split(',') if column])
        data = json.loads(utils.mapper(list(page_data)))

        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num, total_page=pages.num_pages,
                                        present_url=params.present_url,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
