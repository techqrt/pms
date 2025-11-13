import json
from django.db import transaction
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response

from pms.constants import Constants
from pms_apps.common.common import Common
from pms_apps.common.dataclasses.get_all import GetAll
from pms_apps.common.utils import Utils

from pms_apps.property.dataclasses.requests.create import PropertyCreateRequest
from pms_apps.property.dataclasses.requests.update import PropertyUpdateRequest
from pms_apps.property.dataclasses.requests.delete import PropertyDeleteRequest
from pms_apps.property.dataclasses.requests.delete_many import PropertyDeleteManyRequest
from pms_apps.property.dataclasses.requests.get import PropertyGetRequest
from pms_apps.property.utils import PropertyUtils

from pms_apps.property.models.property import Property
from pms_apps.property.serializers.response.get import PropertyGetResponseSerializer
from pms_apps.property.serializers.response.get_all import PropertyGetAllResponseSerializer


class PropertyView:
    def __init__(self) -> None:
        super().__init__()
        self.data_create = "Property added successfully"
        self.data_update = "Property updated successfully"
        self.data_delete = "Property deleted successfully"
        self.data_get = "Property fetched successfully"
        self.data_no_match = "No matching property found"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    # -------------------------------
    # CREATE PROPERTY
    # -------------------------------
    @Common().exception_handler
    def create_extract(self, params: PropertyCreateRequest):
        PropertyUtils.check_constraints(params=params)

        with transaction.atomic():
            data_dict = PropertyUtils.create_extract(params=params)
            Property.create(data=data_dict)

        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(message=self.data_create)
        )

    # -------------------------------
    # UPDATE PROPERTY
    # -------------------------------
    @Common().exception_handler
    def update_extract(self, params: PropertyUpdateRequest):
        property_obj = Property.get(property_id=params.property_id)
        if not property_obj:
            raise ValueError(self.data_no_match)

        with transaction.atomic():
            data_dict = PropertyUtils.update_extract(params=params)
            Property.update(property_id=params.property_id, data=data_dict)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_update)
        )

    # -------------------------------
    # GET SINGLE PROPERTY
    # -------------------------------
    @Common(response_handler=PropertyGetResponseSerializer).exception_handler
    def get_extract(self, params: PropertyGetRequest):
        property_data = Property.get(property_id=params.property_id)
        if not property_data:
            raise ValueError(self.data_no_match)

        utils = PropertyUtils(columns_required=None)
        property_dict = json.loads(utils.mapper([property_data]))[0]

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=property_dict)
        )

    # -------------------------------
    # GET ALL PROPERTIES (Paginated)
    # -------------------------------
    @Common(response_handler=PropertyGetAllResponseSerializer).exception_handler
    def get_all_extract(self, params: GetAll):
        queryset = PropertyUtils.optimized_queryset() 
        pages = Paginator(queryset, params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)

        data = pages.page(params.page_num)
        utils = PropertyUtils(columns_required=None)
        data = json.loads(utils.mapper(data=data))

        final_data = Utils.add_page_parameter(
            final_data=data,
            page_num=params.page_num,
            present_url=params.present_url if hasattr(params, "present_url") else "",
            total_page=pages.num_pages,
            total_count=pages.count,
            next_page_required=(pages.num_pages != params.page_num)
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=final_data)
        )

    # -------------------------------
    # DELETE SINGLE PROPERTY
    # -------------------------------
    @Common().exception_handler
    def delete_extract(self, params: PropertyDeleteRequest):
        property_obj = Property.get(property_id=params.property_id)
        if not property_obj:
            raise ValueError(self.data_no_match)

        with transaction.atomic():
            Property.delete(property_id=params.property_id)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_delete)
        )

    # -------------------------------
    # DELETE MULTIPLE PROPERTIES
    # -------------------------------
    @Common().exception_handler
    def delete_many_extract(self, params: PropertyDeleteManyRequest):
        if not params.ids:
            raise ValueError("Property list is empty. Please provide at least one property ID.")

        queryset = Property.objects.filter(property_id__in=params.ids, is_active=True)
        if queryset.count() != len(params.ids):
            raise ValueError(self.data_no_match)

        with transaction.atomic():
            Property.delete_many(ids=params.ids)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_delete)
        )
