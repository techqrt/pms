from django.db import transaction
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
import json

from pms_apps.common.common import Common
from pms_apps.common.utils import Utils
from pms_apps.common.dataclasses.request.get_all import GetAll
from pms_apps.common.models.permissions import PropertyPermission

from pms_apps.maintenance.models.maintenance_technician import MaintenanceTechnician
from pms_apps.maintenance.dataclasses.request.create.create_technician import MaintenanceTechnicianCreateRequest
from pms_apps.maintenance.dataclasses.request.update.update_technician import MaintenanceTechnicianUpdateRequest
from pms_apps.maintenance.serializers.response.get.get_technician import MaintenanceTechnicianResponseGetSerializer
from pms_apps.maintenance.serializers.response.get_all.get_all_technician import MaintenanceTechnicianResponseGetAllSerializer
from pms_apps.maintenance.utils import MaintenanceUtils


class MaintenanceTechnicianView:
    def __init__(self):
        self.technician_create = "Maintenance technician added successfully"
        self.technician_update = "Maintenance technician updated successfully"
        self.technician_delete = "Maintenance technician deleted successfully"

        self.data_no_match = "No matching record found"
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common().exception_handler
    def create_technician_extract(self, params: MaintenanceTechnicianCreateRequest):
        with transaction.atomic():
            property_permission_id = PropertyPermission().create(
                property=params.permissions.property
            )
            obj = MaintenanceTechnician()
            technician_id = obj.create(
                technician_id=params.technician_id,
                name=params.name,
                dob=params.dob,
                skill_type=params.skill_type,
                years_of_experience=params.years_of_experience,
                assigned_jobs=params.assigned_jobs,
                property_permission_id=property_permission_id,
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(
                message=self.technician_create, data={"technician_id": technician_id})
        )

    @Common().exception_handler
    def update_technician_extract(self, params: MaintenanceTechnicianUpdateRequest):
        with transaction.atomic():
            if params.user_id != params.technician_id:
                raise ValueError("Not allowed to access this resource")
            technician_data = MaintenanceTechnician.get(technician_id=params.technician_id)
            if technician_data is None:
                raise ValueError(self.data_no_match)

            propery_permission_id = None
            if params.permissions:
                if params.permissions.property is not None:
                    propery_permission_id = technician_data.get('property_permission__permission_id')
                    if propery_permission_id:
                        PropertyPermission.update(
                            permission_id=propery_permission_id,
                            property= params.permissions.property
                        )
                    else:
                        propery_permission_id=PropertyPermission().create(
                            property=params.permissions.property
                        )
            
            MaintenanceTechnician.update(
                technician_id=params.technician_id,
                name=params.name,
                dob=params.dob,
                skill_type=params.skill_type,
                years_of_experience=params.years_of_experience,
                assigned_jobs=params.assigned_jobs,
                property_permission_id=propery_permission_id,
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.technician_update))

    @Common().exception_handler
    def delete_technician_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.technician_id:
                raise ValueError("Not allowed to access this resource")
            technician_data = MaintenanceTechnician.get(
                technician_id=params.technician_id)
            if technician_data is None:
                raise ValueError(self.data_no_match)
            MaintenanceTechnician.remove(technician_id=params.technician_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.technician_delete))

    @Common(response_handler=MaintenanceTechnicianResponseGetSerializer).exception_handler
    def get_technician_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.technician_id:
                raise ValueError("Not allowed to access this resource")
            technician_data = MaintenanceTechnician.get(
                technician_id=params.technician_id)
            if technician_data is None:
                raise ValueError(self.data_no_match)
            utils = MaintenanceUtils(entity='technician', columns_required=[
                column for column in params.values.split(',') if column])
            data = json.loads(utils.mapper([technician_data]))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common(response_handler=MaintenanceTechnicianResponseGetAllSerializer).exception_handler
    def get_all_technician_extract(self, params: GetAll):
        reversed_mapped = MaintenanceUtils.reverse_mapper([
            params.sort_by,
            params.filter_key
        ])

        pages = Paginator(MaintenanceTechnician.get_all(
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            filter_key=reversed_mapped.get(params.filter_key),
            filter_value=params.filter_value,
            search_key=params.search_key
        ), per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = pages.page(params.page_num)
        utils = MaintenanceUtils(entity='technician', columns_required=[
            column for column in params.values.split(',') if column])
        data = json.loads(utils.mapper(list(page_data)))

        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num, total_page=pages.num_pages,
                                        present_url=params.present_url,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
