from django.db import transaction
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
import json

from pms_apps.common.common import Common
from pms_apps.common.utils import Utils
from pms_apps.common.dataclasses.request.get_all import GetAll

from pms_apps.owner.models import Owner
from pms_apps.owner.dataclasses.request.create import OwnerCreateRequest
from pms_apps.owner.dataclasses.request.update import OwnerUpdateRequest
from pms_apps.owner.serializers.response.get import OwnerResponseGetSerializer
from pms_apps.owner.serializers.response.get_all import OwnerResponseGetAllSerializer
from pms_apps.owner.utils import OwnerUtils


class OwnerView:
    def __init__(self):
        self.owner_create = "Owner added successfully"
        self.owner_update = "Owner updated successfully"
        self.owner_delete = "Owner deleted successfully"

        self.data_no_match = "No matching record found"
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common().exception_handler
    def create_owner_extract(self, params: OwnerCreateRequest):
        with transaction.atomic():
            obj = Owner()
            owner_id = obj.create(
                owner_id=params.owner_id,
                name=params.name,
                dob=params.dob,
                ownership_type=params.ownership_type,
                properties_owned=params.properties_owned
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(
                message=self.owner_create, data={"owner_id": owner_id})
        )

    @Common().exception_handler
    def update_owner_extract(self, params: OwnerUpdateRequest):
        with transaction.atomic():
            if params.user_id != params.owner_id:
                raise ValueError("Not allowed to access this resource")
            owner_data = Owner.get(owner_id=params.owner_id)
            if owner_data is None:
                raise ValueError(self.data_no_match)

            Owner.update(
                owner_id=params.owner_id,
                name=params.name,
                dob=params.dob,
                ownership_type=params.ownership_type,
                properties_owned=params.properties_owned
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.owner_update))

    @Common().exception_handler
    def delete_owner_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.owner_id:
                raise ValueError("Not allowed to access this resource")
            owner_data = Owner.get(owner_id=params.owner_id)
            if owner_data is None:
                raise ValueError(self.data_no_match)
            Owner.remove(owner_id=params.owner_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.owner_delete))

    @Common(response_handler=OwnerResponseGetSerializer).exception_handler
    def get_owner_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.owner_id:
                raise ValueError("Not allowed to access this resource")
            owner_data = Owner.get(owner_id=params.owner_id)
            if owner_data is None:
                raise ValueError(self.data_no_match)
            utils = OwnerUtils(entity='owner', columns_required=[
                column for column in params.values.split(',') if column])
            data = json.loads(utils.mapper([owner_data]))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common(response_handler=OwnerResponseGetAllSerializer).exception_handler
    def get_all_owner_extract(self, params: GetAll):
        reversed_mapped = OwnerUtils.reverse_mapper([
            params.sort_by,
            params.filter_key
        ])

        pages = Paginator(Owner.get_all(
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            filter_key=reversed_mapped.get(params.filter_key),
            filter_value=params.filter_value,
            search_key=params.search_key
        ), per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = pages.page(params.page_num)
        utils = OwnerUtils(entity='owner', columns_required=[
            column for column in params.values.split(',') if column])
        data = json.loads(utils.mapper(list(page_data)))

        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num, total_page=pages.num_pages,
                                        present_url=params.present_url,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
