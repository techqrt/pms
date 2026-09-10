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
from pms_apps.common.sentinels import NOT_PROVIDED
from pms_apps.authentication.models import User
from pms_apps.lead.dataclasses.request.create import LeadCreateRequest
from pms_apps.lead.dataclasses.request.update import LeadUpdateRequest
from pms_apps.lead.serilizers.response.get import LeadResponseGetSerializer
from pms_apps.lead.serilizers.response.get_all import LeadResponseGetAllSerilizer
from .utils import LeadUtils
from pms_apps.marketing.models.marketing_manager import MarketingManager
from pms_apps.marketing.models.marketing_employee import MarketingEmployee
from pms_apps.checkin_checkout.models.check_in_check_out_manager import CheckInCheckOutManager
from pms_apps.checkin_checkout.models.check_in_check_out_employee import CheckInCheckOutEmployee
from pms_apps.property.image_utils import ImageUtils
from django.core.paginator import Paginator

import json


def _percentage(part: int, total: int) -> float:
    return round((part / total) * 100, 2) if total else 0.0


def _restricted_manager_id(user_id: int):
    """Marketing and Check-In Check-Out are the two departments whose tenant/
    landlord (Lead) access is scoped by assignment (lead_assign_to). Returns
    the caller's manager profile id for whichever one applies, else None."""
    return MarketingManager.get_id(user_id) or CheckInCheckOutManager.get_id(user_id)


def _is_restricted_employee(user_id: int) -> bool:
    return (
        MarketingEmployee.objects.filter(employee_id=user_id).exists()
        or CheckInCheckOutEmployee.objects.filter(employee_id=user_id).exists()
    )


def _assigned_to_ids_for_manager(user_id: int) -> list:
    """A Manager sees leads assigned either to themself or to any Employee
    reporting to them (manager_ref), across Marketing and Check-In Check-Out."""
    ids = {user_id}
    if MarketingManager.get_id(user_id):
        ids.update(
            MarketingEmployee.objects.filter(manager_ref_id=user_id).values_list('employee_id', flat=True)
        )
    if CheckInCheckOutManager.get_id(user_id):
        ids.update(
            CheckInCheckOutEmployee.objects.filter(manager_ref_id=user_id).values_list('employee_id', flat=True)
        )
    return list(ids)


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
                civil_id=params.civil_id,
                purpose=params.purpose,
                po_box=params.po_box,
                feedback=params.feedback,
                lead_category=params.lead_category,
                estimated_closing_date=params.estimated_closing_date,
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
            manager_id = _restricted_manager_id(params.user_id)
            is_employee = _is_restricted_employee(params.user_id)

            if params.user_id != params.lead_id and manager_id is None and not is_employee:
                raise ValueError("Not allowed to access this resource")
            lead_data = Lead.get(lead_id=params.lead_id, include_profile_image=False)
            if lead_data is None:
                raise ValueError(self.data_no_match)
            # A Manager may act on any lead assigned to them or to one of
            # their Employees (so they can reassign it); an Employee (or a
            # non-team caller) must be the lead's exact current assignee.
            if params.user_id != params.lead_id:
                if manager_id:
                    if lead_data.get('lead_assign_to__user_id') not in _assigned_to_ids_for_manager(params.user_id):
                        raise ValueError("Not allowed to access this resource")
                elif lead_data.get('lead_assign_to__user_id') != params.user_id:
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
            if params.profile_picture:
                processed_image = ImageUtils.process_photo(params.profile_picture, upload_path="lead_profiles/")
                # Only set profile_image_obj if it's a valid ContentFile (not a tuple for URLs)
                # Tuples indicate external URLs which shouldn't be stored in ImageField
                if processed_image is not None and not isinstance(processed_image, tuple):
                    profile_image_obj = processed_image

            resolved_lead_assign_to = NOT_PROVIDED
            if params.lead_assign_to is not NOT_PROVIDED:
                user_data = User.get(user_id=params.lead_assign_to)
                resolved_lead_assign_to = user_data.get('user_id') if user_data else None

            if params.phone_number is not NOT_PROVIDED:
                if params.phone_number and User.objects.exclude(user_id=lead_data.get('lead_id')).filter(phone_number=params.phone_number).exists():
                    raise ValueError("Phone number is already in use by another user")
                User.objects.filter(user_id=lead_data.get('lead_id')).update(phone_number=params.phone_number or None)

            Lead.update(
                lead_id=lead_data.get('lead_id'),
                lead_assign_to=resolved_lead_assign_to,
                first_name=params.first_name,
                last_name=params.last_name,
                lead_origin=params.lead_origin,
                address=params.address,
                country_id=params.country_id,
                city_id=params.city_id,
                nationality_id=params.nationality_id,
                passport_or_id=params.passport_or_id,
                civil_id=params.civil_id,
                purpose=params.purpose,
                po_box=params.po_box,
                feedback=params.feedback,
                lead_category=params.lead_category,
                estimated_closing_date=params.estimated_closing_date,
                is_active=params.is_active,
                property_permission_id=property_permission_id,
                profile_image=profile_image_obj,
                email=params.email,
                tenant_code=params.tenant_code,
            )
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_update)
        )

    @Common().exception_handler
    def delete_extract(self, params):
        with transaction.atomic():
            manager_id = _restricted_manager_id(params.user_id)
            is_employee = _is_restricted_employee(params.user_id)

            if params.user_id != params.lead_id and manager_id is None and not is_employee:
                raise ValueError("Not allowed to access this resource")
            lead_data = Lead.get(lead_id=params.lead_id, include_profile_image=False)
            if lead_data is None:
                raise ValueError(self.data_no_match)
            # A Manager may act on any lead assigned to them or to one of
            # their Employees; an Employee (or a non-team caller) must be
            # the lead's exact current assignee.
            if params.user_id != params.lead_id:
                if manager_id:
                    if lead_data.get('lead_assign_to__user_id') not in _assigned_to_ids_for_manager(params.user_id):
                        raise ValueError("Not allowed to access this resource")
                elif lead_data.get('lead_assign_to__user_id') != params.user_id:
                    raise ValueError("Not allowed to access this resource")
            Lead.remove(lead_id=lead_data.get('lead_id'))

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_delete)
        )

    @Common(response_handler=LeadResponseGetSerializer).exception_handler
    def get_extract(self, params):
        with transaction.atomic():
            manager_id = _restricted_manager_id(params.user_id)
            is_employee = _is_restricted_employee(params.user_id)
            if params.user_id != params.lead_id and manager_id is None and not is_employee:
                raise ValueError("Not allowed to access this resource")
            lead_data = Lead.get(lead_id=params.lead_id, include_profile_image=True)
            if lead_data is None:
                raise ValueError(self.data_no_match)
            # A Manager may act on any lead assigned to them or to one of
            # their Employees; an Employee (or a non-team caller) must be
            # the lead's exact current assignee.
            if params.user_id != params.lead_id:
                if manager_id:
                    if lead_data.get('lead_assign_to__user_id') not in _assigned_to_ids_for_manager(params.user_id):
                        raise ValueError("Not allowed to access this resource")
                elif lead_data.get('lead_assign_to__user_id') != params.user_id:
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

            # For Tenant leads, include their currently assigned property
            # (latest non-terminal PropertyAssignment), blank if none.
            data['assignedProperty'] = {}
            if data.get('purpose') == 'Tenant':
                from pms_apps.property.models.property_assignment import PropertyAssignment
                assignment = PropertyAssignment.objects.filter(
                    tenant_id=params.lead_id, is_active=True
                ).exclude(assignment_status__in=["Completed", "Cancelled"]).select_related(
                    'property'
                ).order_by('-assigned_on').first()
                if assignment:
                    data['assignedProperty'] = {
                        'propertyId': assignment.property.property_id,
                        'block': assignment.property.block,
                        'buildingDetails': assignment.property.building_details,
                        'floor': assignment.property.floor,
                        'flatNumber': assignment.property.flat_number,
                    }

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )

    @Common(response_handler=LeadResponseGetAllSerilizer).exception_handler
    def get_all_extract(self,params : GetAll):
        with transaction.atomic():
            manager_id = _restricted_manager_id(params.user_id)
            is_employee = _is_restricted_employee(params.user_id)
            reversed_mapped = LeadUtils.reverse_mapper([
                params.sort_by,
                params.filter_key
            ])

            # Marketing/CICO Managers see leads assigned to them or to their
            # employees; Employees only see leads assigned to them directly.
            if manager_id or is_employee:
                lead_list = Lead.get_all_by_assigned_user(
                    manager_user_id=_assigned_to_ids_for_manager(params.user_id) if manager_id else params.user_id,
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
            
            # Check if no leads assigned to marketing manager/employee
            message = self.data_get
            if (manager_id or is_employee) and not data:
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
        from pms_apps.property.models.property_assignment import PropertyAssignment
        from pms_apps.property.models.property_details import PropertyDetail

        with transaction.atomic():
            manager_id = _restricted_manager_id(params.user_id)
            is_employee = _is_restricted_employee(params.user_id)
            reversed_mapped = LeadUtils.reverse_mapper([
                params.sort_by,
                params.filter_key
            ])

            # Marketing/CICO Managers see leads assigned to them or to their
            # employees; Employees only see leads assigned to them directly.
            if manager_id or is_employee:
                lead_list = Lead.get_all_by_assigned_user(
                    manager_user_id=_assigned_to_ids_for_manager(params.user_id) if manager_id else params.user_id,
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

            # Landlord/Tenant breakdown, keeping every known purpose in the
            # response even when its count is 0 (mirrors property/count/'s byType).
            by_purpose = {choice: 0 for choice, _ in Lead.PURPOSE_CHOICES}
            tenant_ids = set()
            landlord_ids = set()
            for lead in lead_list:
                purpose = lead.get('purpose')
                if purpose in by_purpose:
                    by_purpose[purpose] += 1
                if purpose == 'Tenant':
                    tenant_ids.add(lead['lead_id'])
                elif purpose == 'Landlord':
                    landlord_ids.add(lead['lead_id'])

            # A lead is "converted" once it is actually linked to a property:
            # a Tenant lead via an assignment, a Landlord lead via ownership.
            converted_tenant_count = PropertyAssignment.objects.filter(
                tenant_id__in=tenant_ids
            ).values('tenant_id').distinct().count() if tenant_ids else 0
            converted_landlord_count = PropertyDetail.objects.filter(
                landlord_id__in=landlord_ids
            ).values('landlord_id').distinct().count() if landlord_ids else 0
            converted_count = converted_tenant_count + converted_landlord_count

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message="Total leads count", data={
                "count": lead_count,
                "byPurpose": by_purpose,
                "convertedCount": converted_count,
                "conversionRate": _percentage(converted_count, lead_count),
            })
        )
