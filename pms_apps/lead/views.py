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
from pms_apps.marketing.models.marketing_manager import MarketingManager
from pms_apps.property.image_utils import ImageUtils
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
            # Create a new user for the lead
            new_user = User()
            new_user.phone_number = params.phone_number
            new_user.name = f"{params.first_name} {params.last_name}"
            new_user.department = params.purpose
            new_user.save()
            
            lead_permission = PropertyPermission()
            lead_permission.property = True
            lead_permission.save()
            
            # Process profile picture if provided
            profile_image_obj = None
            if params.profile_picture:
                processed_image = ImageUtils.process_photo(params.profile_picture, upload_path="lead_profiles/")
                # Only set profile_image_obj if it's a valid ContentFile (not a tuple for URLs)
                # Tuples indicate external URLs which shouldn't be stored in ImageField
                if processed_image is not None and not isinstance(processed_image, tuple):
                    profile_image_obj = processed_image
            
            lead = Lead()
            lead_id = lead.create(
                lead_id=new_user.user_id,
                lead_assign_to=params.lead_assign_to,
                first_name=params.first_name,
                last_name=params.last_name,
                lead_origin=params.lead_origin,
                address=params.address,
                country_id=params.country_id,
                city_id=params.city_id,
                nationality_id=params.nationality_id,
                passport_or_id=params.passport_or_id,
                purpose=params.purpose,
                po_box=params.po_box,
                feedback=params.feedback,
                lead_category=params.lead_category,
                property_permissions_id=lead_permission.permission_id,
                profile_image=profile_image_obj
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
            manager_id = MarketingManager.get_id(params.user_id)

            
            if params.user_id != params.lead_id and params.user_id != manager_id:
                raise ValueError("Not allowed to access this resource")
            user_data = User.get(user_id=params.lead_assign_to)
            lead_data = Lead.get(lead_id=params.lead_id, include_profile_image=False)
            if lead_data is None:
                raise ValueError(self.data_no_match)
            # If marketing manager, verify lead is assigned to them
            if manager_id and params.user_id == manager_id:
                if lead_data.get('lead_assign_to__user_id') != params.user_id:
                    raise ValueError("Not allowed to access this resource")

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

            # Process profile picture if provided
            profile_image_obj = None
            if params.profile_picture is not None:
                processed_image = ImageUtils.process_photo(params.profile_picture, upload_path="lead_profiles/")
                # Only set profile_image_obj if it's a valid ContentFile (not a tuple for URLs)
                # Tuples indicate external URLs which shouldn't be stored in ImageField
                if processed_image is not None and not isinstance(processed_image, tuple):
                    profile_image_obj = processed_image

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
                po_box=params.po_box,
                feedback=params.feedback,
                lead_category=params.lead_category,
                is_active=params.is_active,
                property_permission_id=property_permission_id,
                profile_image=profile_image_obj,
                email=params.email,
            )
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_update)
        )

    @Common().exception_handler
    def delete_extract(self, params):
        with transaction.atomic():
            manager_id = MarketingManager.get_id(params.user_id)
            
            if params.user_id != params.lead_id and params.user_id != manager_id:
                raise ValueError("Not allowed to access this resource")
            lead_data = Lead.get(lead_id=params.lead_id, include_profile_image=False)
            if lead_data is None:
                raise ValueError(self.data_no_match)
            # If marketing manager, verify lead is assigned to them
            if manager_id and params.user_id == manager_id:
                if lead_data.get('lead_assign_to__user_id') != params.user_id:
                    raise ValueError("Not allowed to access this resource")
            Lead.remove(lead_id=lead_data.get('lead_id'))

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_delete)
        )

    @Common(response_handler=LeadResponseGetSerializer).exception_handler
    def get_extract(self, params):
        with transaction.atomic():
            manager_id = MarketingManager.get_id(params.user_id)
            if params.user_id != params.lead_id and params.user_id != manager_id:
                raise ValueError("Not allowed to access this resource")
            lead_data = Lead.get(lead_id=params.lead_id, include_profile_image=True)
            if lead_data is None:
                raise ValueError(self.data_no_match)
            # If marketing manager, verify lead is assigned to them
            if manager_id and params.user_id == manager_id:
                if lead_data.get('lead_assign_to__user_id') != params.user_id:
                    raise ValueError("Not allowed to access this resource")

            columns = [column for column in params.values.split(',') if column]
            # Auto-include lead_assign_to__name when lead_assign_to__user_id is requested
            if 'lead_assign_to__user_id' in columns and 'lead_assign_to__name' not in columns:
                columns.append('lead_assign_to__name')
            # Auto-include lead_id__phone_number when lead_id is requested
            if 'lead_id' in columns and 'lead_id__phone_number' not in columns:
                columns.append('lead_id__phone_number')
            
            lead_utils = LeadUtils(columns_required=columns)
            lead_data = [lead_data]
            data = json.loads(lead_utils.mapper(lead_data))[0]

            # Add profile picture URL if available
            from pms_apps.lead.models.lead import Lead as LeadModel
            lead_obj = LeadModel.objects.filter(lead_id=params.lead_id).first()
            if lead_obj and lead_obj.profile_image:
                profile_image_value = str(lead_obj.profile_image)
                # Check if it's already a URL
                if profile_image_value.startswith('http://') or profile_image_value.startswith('https://'):
                    data['profileImage'] = profile_image_value
                else:
                    # It's a file path managed by Django
                    profile_image_url = ImageUtils.get_photo_url(profile_image_value)
                    if profile_image_url:
                        data['profileImage'] = profile_image_url

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )

    @Common(response_handler=LeadResponseGetAllSerilizer).exception_handler
    def get_all_extract(self,params : GetAll):
        with transaction.atomic():
            manager_id = MarketingManager.get_id(params.user_id)
            reversed_mapped = LeadUtils.reverse_mapper([
                params.sort_by,
                params.filter_key
            ])

            # If marketing manager, get only leads assigned to them
            if manager_id:
                lead_list = Lead.get_all_by_assigned_user(
                    manager_user_id=params.user_id,
                    sort_by=reversed_mapped.get(params.sort_by),
                    sort_order=params.sort_order,
                    filter_key=reversed_mapped.get(params.filter_key),
                    filter_value=params.filter_value,
                    search_key=params.search_key
                )
            else:
                lead_list = Lead.get_all(
                    sort_by=reversed_mapped.get(params.sort_by),
                    sort_order=params.sort_order,
                    filter_key=reversed_mapped.get(params.filter_key),
                    filter_value=params.filter_value,
                    search_key=params.search_key
                )
            
            pages = Paginator(lead_list, per_page=params.limit)

            if pages.num_pages < params.page_num:
                raise ValueError('Page limit exceed!')
                
            data = pages.page(params.page_num)
            columns = [column for column in params.values.split(',') if column]
            # Auto-include lead_assign_to__name when lead_assign_to__user_id is requested
            if 'lead_assign_to__user_id' in columns and 'lead_assign_to__name' not in columns:
                columns.append('lead_assign_to__name')
            # Auto-include lead_id__phone_number when lead_id is requested
            if 'lead_id' in columns and 'lead_id__phone_number' not in columns:
                columns.append('lead_id__phone_number')
            
            lead_utils = LeadUtils(columns_required=columns)
            data = json.loads(lead_utils.mapper(data=data))
            
            # Convert profile_image to URLs if present and if 'profile_image' was in columns
            if 'profile_image' in columns and data:
                from pms_apps.lead.models.lead import Lead as LeadModel
                lead_ids = [item.get('leadId') for item in data if item.get('leadId')]
                if lead_ids:
                    lead_objects = LeadModel.objects.filter(lead_id__in=lead_ids)
                    profile_image_map = {
                        lead.lead_id: (
                            ImageUtils.get_photo_url(str(lead.profile_image))
                            if lead.profile_image and not str(lead.profile_image).startswith(('http://', 'https://'))
                            else str(lead.profile_image) if lead.profile_image else None
                        )
                        for lead in lead_objects
                    }
                    for item in data:
                        lead_id = item.get('leadId')
                        if lead_id in profile_image_map:
                            item['profileImage'] = profile_image_map[lead_id]
            
            # Check if no leads assigned to marketing manager
            message = self.data_get
            if manager_id and not data:
                message = "You don't have any leads assigned to you"
    
            data = Utils.add_page_parameter(    
                final_data=data,
                page_num=params.page_num,
                total_page=pages.num_pages,
                present_url=params.present_url,
                next_page_required=True if pages.num_pages != params.page_num else False)
            
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=message, data=data)
        )

    @Common().exception_handler
    def count_extract(self, params: GetAll):
        with transaction.atomic():
            manager_id = MarketingManager.get_id(params.user_id)
            reversed_mapped = LeadUtils.reverse_mapper([
                params.sort_by,
                params.filter_key
            ])

            # If marketing manager, get only leads assigned to them
            if manager_id:
                lead_list = Lead.get_all_by_assigned_user(
                    manager_user_id=params.user_id,
                    sort_by=reversed_mapped.get(params.sort_by),
                    sort_order=params.sort_order,
                    filter_key=reversed_mapped.get(params.filter_key),
                    filter_value=params.filter_value,
                    search_key=params.search_key
                )
            else:
                lead_list = Lead.get_all(
                    sort_by=reversed_mapped.get(params.sort_by),
                    sort_order=params.sort_order,
                    filter_key=reversed_mapped.get(params.filter_key),
                    filter_value=params.filter_value,
                    search_key=params.search_key
                )
            
            lead_count = len(lead_list)
            
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message="Total leads count", data={"count": lead_count})
        )
