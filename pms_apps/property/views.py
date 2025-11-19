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
from pms_apps.property.serializers.response.get import PropertyResponseGetSerializer
from pms_apps.property.serializers.response.get_all import PropertyResponseGetAllSerializer

from pms_apps.authentication.models import User


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

    @Common().exception_handler
    def create_extract(self, params: PropertyCreateRequest):
        PropertyUtils.check_constraints(params=params)
        with transaction.atomic():
            property = Property()
            property_id = property.create(
                block = params.block,
                building_details=params.building_details,
                floor = params.floor,
                flat_number = params.flat_number,
                dimension_length_ft = params.dimension_length_ft,
                dimension_breadth_ft = params.dimension_breadth_ft,
                dimension_area_sqft = params.dimension_area_sqft,
                rental_type = params.rental_type,
                hall = params.hall,
                bedroom_count = params.bedroom_count,
                kitchen = params.kitchen,
                attached_bathroom_count = params.attached_bathroom_count,
                single_bathroom_count = params.single_bathroom_count,
                balcony  = params.balcony,
                store_room = params.store_room,
                rental_for = params.rental_for,
                advance_amount_rent = params.advance_amount_rent,
                expected_rent = params.expected_rent,
                agreement_id = params.agreement_id,
                photos = params.photos,
                videos = params.videos,
                created_by = params.user_id,
            )

        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(message=self.data_create,data={'property_id' : property_id})
        )

    @Common().exception_handler
    def update_extract(self, params: PropertyUpdateRequest):
        PropertyUtils.check_constraints(params=params)
        assigned_to_user = None
        if params.assigned_to:
            assigned_to_user = User.get(user_id=params.assigned_to)
        
    
        property_obj = Property.get(property_id=params.property_id)
        if not property_obj:
            raise ValueError(self.data_no_match)
        
        print(params)

        with transaction.atomic():
            Property.update(
                property_id=params.property_id,
                block = params.block,
                building_details=params.building_details,
                floor = params.floor,
                flat_number = params.flat_number,
                dimension_length_ft = params.dimension_length_ft,
                dimension_breadth_ft = params.dimension_breadth_ft,
                dimension_area_sqft = params.dimension_area_sqft,
                rental_type = params.rental_type,
                hall = params.hall,
                bedroom_count = params.bedroom_count,
                kitchen = params.kitchen,
                attached_bathroom_count = params.attached_bathroom_count,
                single_bathroom_count = params.single_bathroom_count,
                balcony  = params.balcony,
                store_room = params.store_room,
                rental_for = params.rental_for,
                advance_amount_rent = params.advance_amount_rent,
                expected_rent = params.expected_rent,
                agreement_id = params.agreement_id,
                photos = params.photos,
                videos = params.videos,
                assigned_to = assigned_to_user.get('user_id') if assigned_to_user else None,
            )
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_update)
        )

    @Common(response_handler=PropertyResponseGetSerializer).exception_handler
    def get_extract(self, params: PropertyGetRequest):
        property_data = Property.get(property_id=params.property_id)
        if not property_data:
            raise ValueError(self.data_no_match)

        utils = PropertyUtils(columns_required=[column for column in params.values.split(',') if column])
        property_dict = json.loads(utils.mapper([property_data]))[0]

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=property_dict)
        )

    @Common(response_handler=PropertyResponseGetAllSerializer).exception_handler
    def get_all_extract(self, params: GetAll):
        reversed_mapped = PropertyUtils.reverse_mapper([
            params.sort_by,
            params.filter_key
        ])

        
        pages = Paginator(Property.get_all(
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            filter_key=reversed_mapped.get(params.filter_key),
            filter_value=params.filter_value,
            search_key=params.search_key
        ),per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)

        data = pages.page(params.page_num)
        utils = PropertyUtils(columns_required=[column for column in params.values.split(',') if column])
        data = json.loads(utils.mapper(data=data))

        data = Utils.add_page_parameter(
            final_data=data,
            page_num=params.page_num,
            total_page=pages.num_pages,
            present_url=params.present_url,
            next_page_required=True if pages.num_pages != params.page_num else False
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )

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

    @Common().exception_handler
    def delete_many_extract(self, params: PropertyDeleteManyRequest):
        if not params.property_ids:
            raise ValueError("Property list is empty. Please provide at least one property ID.")

        queryset = Property.objects.filter(property_id__in=params.property_ids, is_active=True)
        if queryset.count() != len(params.property_ids):
            raise ValueError(self.data_no_match)

        with transaction.atomic():
            Property.delete_many(ids=params.property_ids)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_delete)
        )
