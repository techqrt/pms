from .models.lead import Lead
from pms_apps.common.models.permissions import PropertyPermission
from django.db import transaction
from pms_apps.common.common import Common
from rest_framework.response import Response
from rest_framework import status
from pms_apps.common.utils import Utils
from pms_apps.helper_apis.models.city import City
from pms_apps.helper_apis.models.country import Country
from pms_apps.common.dataclasses.request.get_all import GetAll
from pms_apps.authentication.models import User
from pms_apps.lead.dataclasses.request.create import LeadCreateRequest
from pms_apps.lead.dataclasses.request.update import LeadUpdateRequest
from pms_apps.lead.serilizers.response.get import LeadResponseGetSerializer
from pms_apps.lead.serilizers.response.get_all import LeadResponseGetAllSerilizer
from .utils import LeadUtils
from django.core.paginator import Paginator

import json


class LeadView:
    def __init__(self):
        self.data_create = "Lead added successfully"
        self.data_update = "Lead updated successfully"
        self.data_delete = "Lead deleted successfully"
        self.data_no_match = "No matching lead found"
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common().exception_handler
    @Common().country_city_validation
    def create_extract(self, params: LeadCreateRequest):
        
        with transaction.atomic():
            user_data = User.get(user_id=params.lead_assign_to)

            if not user_data:
                raise ValueError(f'Invalid User id : {params.lead_assign_to}')

            lead_permission = PropertyPermission()
            lead_permission.property = True
            lead_permission.save()
            lead = Lead()
            lead_id = lead.create(
                lead_id=params.user_id,
                lead_assign_to=user_data.get('user_id'),
                first_name=params.first_name,
                last_name=params.last_name,
                lead_origin=params.lead_origin,
                address=params.address,
                country_id=params.country_id,
                city_id=params.city_id,
                nationality_id=params.nationality_id,
                passport_or_id=params.passport_or_id,
                purpose=params.purpose,
                property_permissions_id=lead_permission.permission_id
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(message=self.data_create, data={
                                             "lead_id": lead_id.user_id})
        )

    @Common().exception_handler
    @Common().country_city_validation
    def update_extract(self, params: LeadUpdateRequest):
        with transaction.atomic():
            if params.user_id != params.lead_id:
                raise ValueError("Not allowed to access this resource")
            user_data = User.get(user_id=params.lead_assign_to)
            lead_data = Lead.get(lead_id=params.lead_id)
            if lead_data is None:
                raise ValueError(self.data_no_match)

            property_permission_id = None
            if params.property_permission:
                property_permission_id = lead_data.get(
                    "property_permissions__permission_id")
                
                if not property_permission_id:
                    property_permission_id = PropertyPermission().create(property=params.property_permission.property)
                else:
                    PropertyPermission.update(
                        permission_id=property_permission_id,
                        property=params.property_permission.property
                    )
                    property_permission_id = property_permission_id

            Lead.update(
                lead_id=lead_data.get('lead_id'),
                lead_assign_to=user_data.get('user_id') if user_data else None,
                first_name=params.first_name,
                last_name=params.last_name,
                lead_origin=params.lead_origin,
                address=params.address,
                country_id=params.country_id,
                city_id=params.city_id,
                nationality_id=params.nationality_id,
                passport_or_id=params.passport_or_id,
                purpose=params.purpose,
                property_permission_id=property_permission_id
            )
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_update)
        )

    @Common().exception_handler
    def delete_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.lead_id:
                raise ValueError("Not allowed to access this resource")
            lead_data = Lead.get(lead_id=params.lead_id)
            if lead_data is None:
                raise ValueError(self.data_no_match)
            Lead.remove(lead_id=lead_data.get('lead_id'))

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_delete)
        )

    @Common(response_handler=LeadResponseGetSerializer).exception_handler
    def get_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.lead_id:
                raise ValueError("Not allowed to access this resource")
            lead_data = Lead.get(lead_id=params.lead_id)
            if lead_data is None:
                raise ValueError(self.data_no_match)

            lead_utils = LeadUtils(
                columns_required=[column for column in params.values.split(',') if column])
            lead_data = [lead_data]
            data = json.loads(lead_utils.mapper(lead_data))[0]

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )

    @Common(response_handler=LeadResponseGetAllSerilizer).exception_handler
    def get_all_extract(self,params : GetAll):
        with transaction.atomic():
            reversed_mapped = LeadUtils.reverse_mapper([
                params.sort_by,
                params.filter_key
            ])

            pages = Paginator(Lead.get_all(
                sort_by=reversed_mapped.get(params.sort_by),
                sort_order=params.sort_order,
                filter_key=reversed_mapped.get(params.filter_key),
                filter_value=params.filter_value,
                search_key=params.search_key
            ),per_page=params.limit)

            if pages.num_pages < params.page_num:
                raise ValueError('Page limit exceed!')
                
            data = pages.page(params.page_num)
            lead_utils = LeadUtils(columns_required=[column for column in params.values.split(',') if column])
            data = json.loads(lead_utils.mapper(data=data))

            data = Utils.add_page_parameter(
                final_data=data,
                page_num=params.page_num,
                total_page=pages.num_pages,
                present_url=params.present_url,
                next_page_required=True if pages.num_pages != params.page_num else False)
            
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )
