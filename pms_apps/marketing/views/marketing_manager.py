from django.db import transaction
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
import json

from pms_apps.common.common import Common
from pms_apps.common.utils import Utils
from pms_apps.common.dataclasses.request.get_all import GetAll

from pms_apps.marketing.models.marketing_manager import MarketingManager
from pms_apps.marketing.dataclasses.request.create.create_manager import MarketingManagerCreateRequest
from pms_apps.marketing.dataclasses.request.update.update_manager import MarketingManagerUpdateRequest
from pms_apps.marketing.serializers.response.get.get_manager import MarketingManagerResponseGetSerializer
from pms_apps.marketing.serializers.response.get_all.get_all_manager import MarketingManagerResponseGetAllSerializer

from pms_apps.marketing.utils import MarketingUtils
from pms_apps.common.models.permissions import LeadPermission,PropertyPermission
from pms_apps.authentication.models import User
from pms_apps.property.image_utils import ImageUtils


class MarketingManagerView:
    def __init__(self):
        self.manager_create = "Marketing manager added successfully"
        self.manager_update = "Marketing manager updated successfully"
        self.manager_delete = "Marketing manager deleted successfully"

        self.data_no_match = "No matching record found"
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common().exception_handler
    def create_manager_extract(self, params: MarketingManagerCreateRequest):
        with transaction.atomic():
            lead_permission_id = LeadPermission().create(
                lead=params.permissions.lead
            )
            property_permission_id = PropertyPermission().create(
                property=params.permissions.property
            )

            # Process profile picture if provided
            profile_picture_obj = None
            if params.profile_picture:
                profile_picture_obj = ImageUtils.process_photo(params.profile_picture, upload_path="marketing_manager_profiles/")

            obj = MarketingManager()
            manager_id = obj.create(
                manager_id=params.manager_id,
                name=params.name,
                dob=params.dob,
                department=params.department,
                campaigns_led=params.campaigns_led,
                team_size=params.team_size,
                lead_permission_id=lead_permission_id,
                property_permission_id=property_permission_id,
                profile_picture=profile_picture_obj
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(
                message=self.manager_create, data={"manager_id": manager_id})
        )

    @Common().exception_handler
    def update_manager_extract(self, params: MarketingManagerUpdateRequest):
        with transaction.atomic():
            if params.user_id != params.manager_id:
                raise ValueError("Not allowed to access this resource")
            if params.user_id != params.manager_id:
                raise ValueError("Not allowed to access this resource")
            manager_data = MarketingManager.get(manager_id=params.manager_id)
            if manager_data is None:
                raise ValueError(self.data_no_match)

            # Update User table with phone_number and email
            if params.phone_number is not None or params.email is not None:
                user_update_data = {}
                if params.phone_number is not None:
                    user_update_data['phone_number'] = params.phone_number
                if params.email is not None:
                    user_update_data['email'] = params.email
                if user_update_data:
                    User.objects.filter(user_id=params.manager_id).update(**user_update_data)

            # Process profile picture if provided
            profile_picture_obj = None
            if params.profile_picture is not None:
                profile_picture_obj = ImageUtils.process_photo(params.profile_picture, upload_path="marketing_manager_profiles/")

            lead_permission_id = None
            propery_permission_id = None
            if params.permissions:
                if params.permissions.lead is not None:
                    lead_permission_id = manager_data.get('lead_permission__permission_id')
                    if lead_permission_id:
                        LeadPermission.update(
                            permission_id=lead_permission_id,
                            lead=params.permissions.lead
                        )
                    else:
                        lead_permission_id = LeadPermission().create(
                            lead=params.permissions.lead
                        )
                if params.permissions.property is not None:
                    propery_permission_id = manager_data.get('property_permission__permission_id')
                    if propery_permission_id:
                        PropertyPermission.update(
                            permission_id=propery_permission_id,
                            property= params.permissions.property
                        )
                    else:
                        propery_permission_id=PropertyPermission().create(
                            property=params.permissions.property
                        )

            MarketingManager.update(
                manager_id=params.manager_id,
                name=params.name,
                dob=params.dob,
                department=params.department,
                campaigns_led=params.campaigns_led,
                team_size=params.team_size,
                property_permission_id=propery_permission_id,
                lead_permission_id=lead_permission_id,
                profile_picture=profile_picture_obj
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.manager_update))

    @Common().exception_handler
    def delete_manager_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.manager_id:
                raise ValueError("Not allowed to access this resource")
            if params.user_id != params.manager_id:
                raise ValueError("Not allowed to access this resource")
            manager_data = MarketingManager.get(manager_id=params.manager_id)
            if manager_data is None:
                raise ValueError(self.data_no_match)
            MarketingManager.remove(manager_id=params.manager_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.manager_delete))

    @Common(response_handler=MarketingManagerResponseGetSerializer).exception_handler
    def get_manager_extract(self, params):
        with transaction.atomic():
            if params.user_id != params.manager_id:
                raise ValueError("Not allowed to access this resource")
            manager_data = MarketingManager.get(manager_id=params.manager_id)
            if manager_data is None:
                raise ValueError(self.data_no_match)
            marketing_utils = MarketingUtils(entity='manager', columns_required=[
                                             column for column in params.values.split(',') if column])
            data = json.loads(marketing_utils.mapper([manager_data]))[0]
            
            # Process profile picture URL
            if manager_data.get('profile_picture'):
                profile_picture_path = str(manager_data.get('profile_picture'))
                if profile_picture_path.startswith('http://') or profile_picture_path.startswith('https://'):
                    data['profilePicture'] = profile_picture_path
                else:
                    photo_url = ImageUtils.get_photo_url(profile_picture_path)
                    if photo_url:
                        data['profilePicture'] = photo_url
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common(response_handler=MarketingManagerResponseGetAllSerializer).exception_handler
    def get_all_manager_extract(self, params: GetAll):
        reversed_mapped = MarketingUtils.reverse_mapper([
            params.sort_by,
            params.filter_key
        ])

        manager_list = MarketingManager.get_all(
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            filter_key=reversed_mapped.get(params.filter_key),
            filter_value=params.filter_value,
            search_key=params.search_key
        )
        
        pages = Paginator(manager_list, per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = pages.page(params.page_num)
        utils = MarketingUtils(entity='manager', columns_required=[
                               column for column in params.values.split(',') if column])
        data = json.loads(utils.mapper(list(page_data)))

        # Process profile picture URLs for each manager
        page_managers_dict = {m['manager_id']: m for m in page_data if m}
        
        for item in data:
            manager_id = item.get('managerId')
            if manager_id in page_managers_dict:
                manager_data = page_managers_dict[manager_id]
                if manager_data.get('profile_picture'):
                    profile_picture_path = str(manager_data.get('profile_picture'))
                    if profile_picture_path.startswith('http://') or profile_picture_path.startswith('https://'):
                        item['profilePicture'] = profile_picture_path
                    else:
                        photo_url = ImageUtils.get_photo_url(profile_picture_path)
                        if photo_url:
                            item['profilePicture'] = photo_url

        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num, total_page=pages.num_pages,
                                        present_url=params.present_url,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
