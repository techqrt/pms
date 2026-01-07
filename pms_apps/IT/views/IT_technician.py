from django.db import transaction
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
import json

from pms_apps.common.common import Common
from pms_apps.common.utils import Utils
from pms_apps.common.dataclasses.request.get_all import GetAll

from pms_apps.IT.models.IT_technician import ITTechnician
from pms_apps.IT.dataclasses.request.create.create_technician import ITTechnicianCreateRequest
from pms_apps.IT.dataclasses.request.update.update_technician import ITTechnicianUpdateRequest
from pms_apps.IT.serializers.response.get.get_technician import ITTechnicianResponseGetSerializer
from pms_apps.IT.serializers.response.get_all.get_all_technician import ITTechnicianResponseGetAllSerializer
from pms_apps.IT.utils import ITUtils


class ITTechnicianView:
    def __init__(self):
        self.technician_create = "IT technician added successfully"
        self.technician_update = "IT technician updated successfully"
        self.technician_delete = "IT technician deleted successfully"

        self.data_no_match = "No matching record found"
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common().exception_handler
    def create_technician_extract(self, params: ITTechnicianCreateRequest):
        with transaction.atomic():
            obj = ITTechnician()
            technician_id = obj.create(
                technician_id=params.technician_id,
                name=params.name,
                dob=params.dob,
                skill_area=params.skill_area,
                tickets_closed=params.tickets_closed,
                years_of_experience=params.years_of_experience
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(
                message=self.technician_create, data={"technician_id": technician_id})
        )

    @Common().exception_handler
    def update_technician_extract(self, params: ITTechnicianUpdateRequest):
        with transaction.atomic():
            if params.user_id != params.technician_id:
                raise ValueError("Not allowed to access this resource")
            technician_data = ITTechnician.get(
                technician_id=params.technician_id)
            if technician_data is None:
                raise ValueError(self.data_no_match)

            ITTechnician.update(
                technician_id=params.technician_id,
                name=params.name,
                dob=params.dob,
                skill_area=params.skill_area,
                tickets_closed=params.tickets_closed,
                years_of_experience=params.years_of_experience
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.technician_update))

    @Common().exception_handler
    def delete_technician_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.technician_id:
                raise ValueError("Not allowed to access this resource")
            technician_data = ITTechnician.get(
                technician_id=params.technician_id)
            if technician_data is None:
                raise ValueError(self.data_no_match)
            ITTechnician.remove(technician_id=params.technician_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.technician_delete))

    @Common(response_handler=ITTechnicianResponseGetSerializer).exception_handler
    def get_technician_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.technician_id:
                raise ValueError("Not allowed to access this resource")
            technician_data = ITTechnician.get(
                technician_id=params.technician_id)
            if technician_data is None:
                raise ValueError(self.data_no_match)
            utils = ITUtils(entity='technician', columns_required=[
                column for column in params.values.split(',') if column])
            data = json.loads(utils.mapper([technician_data]))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common(response_handler=ITTechnicianResponseGetAllSerializer).exception_handler
    def get_all_technician_extract(self, params: GetAll):
        reversed_mapped = ITUtils.reverse_mapper([
            params.sort_by,
            params.filter_key
        ])

        pages = Paginator(ITTechnician.get_all(
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            filter_key=reversed_mapped.get(params.filter_key),
            filter_value=params.filter_value,
            search_key=params.search_key
        ), per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = pages.page(params.page_num)
        utils = ITUtils(entity='technician', columns_required=[
            column for column in params.values.split(',') if column])
        data = json.loads(utils.mapper(list(page_data)))

        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num, total_page=pages.num_pages,
                                        present_url=params.present_url,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
