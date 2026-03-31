import json
from django.db import transaction
from django.db.models import Q
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
from pms_apps.property.dataclasses.requests.property_assignment_create import PropertyAssignmentCreateRequest
from pms_apps.property.utils import PropertyUtils

from pms_apps.property.models.property import Property
from pms_apps.property.serializers.response.get import PropertyResponseGetSerializer
from pms_apps.property.serializers.response.get_all import PropertyResponseGetAllSerializer
from pms_apps.property.serializers.response.assignment_get import PropertyAssignmentResponseGetSerializer
from pms_apps.property.serializers.response.assignment_get_all import PropertyAssignmentResponseGetAllSerializer

from pms_apps.authentication.models import User
from pms_apps.property.models.property_details import PropertyDetail
from pms_apps.property.models.property_assignment import PropertyAssignment
from pms_apps.marketing.models.marketing_manager import MarketingManager

class PropertyView:
    def __init__(self) -> None:
        super().__init__()
        self.data_create = "Property added successfully"
        self.data_update = "Property updated successfully"
        self.data_delete = "Property deleted successfully"
        self.data_get = "Property fetched successfully"
        self.data_no_match = "No matching property found"
        self.data_assign = "Property assigned to tenant successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common().exception_handler
    def create_extract(self, params: PropertyCreateRequest):
        PropertyUtils.check_constraints(params=params)
        
        # Mirror nested data to root Property fields for cleaner visibility
        block = params.block or params.property_details.address_line_2
        building_details = params.building_details or params.property_details.building_name
        
        floor = params.floor
        if not floor:
            if params.rental_type == 'Flat' and params.flat_data:
                floor = str(params.flat_data.floor_number) if params.flat_data.floor_number else None
            elif params.rental_type == 'Commercial' and params.commercial_data:
                floor = str(params.commercial_data.floor_number) if params.commercial_data.floor_number else None

        flat_number = params.flat_number
        if not flat_number and params.rental_type == 'Flat' and params.flat_data:
            # Try to convert flat string to int safely if possible
            try:
                import re
                nums = re.findall(r'\d+', params.flat_data.flat_number)
                if nums:
                    flat_number = int(nums[0])
            except (ValueError, TypeError):
                pass

        with transaction.atomic():
            property = Property()
            property_id = property.create(
                block=block,
                building_details=building_details,
                floor=floor,
                flat_number=flat_number,
                dimension_length_ft=params.dimension_length_ft,
                dimension_breadth_ft=params.dimension_breadth_ft,
                dimension_area_sqft=params.dimension_area_sqft,
                rental_type=params.rental_type,
                rental_for=params.rental_for,
                advance_amount_rent=params.advance_amount_rent,
                expected_rent=params.expected_rent,
                agreement_id=params.agreement_id,
                created_by=params.user_id or params.property_details.created_by_id,
            )

            from pms_apps.property.models.property_details import PropertyDetail
            
            property_detail_kwargs = {
                'property_id': property_id,
                'building_name': params.property_details.building_name,
                'total_floors': params.property_details.total_floors,
                'carpet_area_sqft': params.property_details.carpet_area_sqft,
                'builtup_area_sqft': params.property_details.builtup_area_sqft,
                'monthly_rent': params.property_details.monthly_rent,
                'security_deposit_amount': params.property_details.security_deposit_amount,
                'electricity_charge_type': params.property_details.electricity_charge_type,
                'water_charge_type': params.property_details.water_charge_type,
                'late_fee_type': params.property_details.late_fee_type,
                'late_fee_value': params.property_details.late_fee_value,
                'current_status': params.property_details.current_status,
                'landlord_id': params.property_details.landlord_id,
                'created_by_id': params.property_details.created_by_id,
                'address_line_1': params.property_details.address_line_1,
                'area_zone': params.property_details.area_zone,
                'city': params.property_details.city,
                'state': params.property_details.state,
                'country': params.property_details.country,
                'pincode': params.property_details.pincode,
                'google_map_location': params.property_details.google_map_location,
                'year_of_construction': params.property_details.year_of_construction,
                'other_charges': params.property_details.other_charges,
                'available_from': params.property_details.available_from,
                'current_tenant_id': params.property_details.current_tenant_id,
                'address_line_2': params.property_details.address_line_2,
                'internal_notes': params.property_details.internal_notes,
            }

            # Add rental type-specific data
            if params.rental_type == 'Flat' and params.flat_data:
                property_detail_kwargs.update({
                    'flat_number': params.flat_data.flat_number,
                    'floor_number': params.flat_data.floor_number,
                    'building_block': params.flat_data.building_block,
                    'flat_configuration': params.flat_data.flat_configuration,
                    'no_of_bathrooms': params.flat_data.no_of_bathrooms,
                    'kitchen_type': params.flat_data.kitchen_type,
                    'facing': params.flat_data.facing,
                    'balcony': params.flat_data.balcony,
                    'parking': params.flat_data.parking,
                    'lift': params.flat_data.lift,
                    'security': params.flat_data.security,
                    'gas_pipeline': params.flat_data.gas_pipeline,
                    'water_supply': params.flat_data.water_supply,
                    'intercom': params.flat_data.intercom,
                    'fire_safety': params.flat_data.fire_safety,
                    'power_backup': params.flat_data.power_backup,
                    'cctv': params.flat_data.cctv,
                    'allowed_tenant_types': params.flat_data.allowed_tenant_types,
                    'store_room': params.flat_data.store_room,
                    'maintenance_charge_amount': params.flat_data.maintenance_charge_amount,
                    'electricity_charge_amount': params.flat_data.electricity_charge_amount,
                    'water_charge_amount': params.flat_data.water_charge_amount,
                })
            elif params.rental_type == 'Commercial' and params.commercial_data:
                property_detail_kwargs.update({
                    'commercial_category': params.commercial_data.commercial_category,
                    'floor_number': params.commercial_data.floor_number,
                    'frontage_width_ft': params.commercial_data.frontage_width_ft,
                    'ceiling_height_ft': params.commercial_data.ceiling_height_ft,
                    'no_of_cabins': params.commercial_data.no_of_cabins,
                    'no_of_washrooms': params.commercial_data.no_of_washrooms,
                    'loading_area': params.commercial_data.loading_area,
                    'power_load_kw': params.commercial_data.power_load_kw,
                    'has_dg_backup': params.commercial_data.has_dg_backup,
                    'lift_type': params.commercial_data.lift_type,
                    'fire_safety_compliant': params.commercial_data.fire_safety_compliant,
                    'emergency_exit': params.commercial_data.emergency_exit,
                    'parking_availability': params.commercial_data.parking_availability,
                    'commercial_maintenance_charge_type': params.commercial_data.commercial_maintenance_charge_type,
                    'gst_applicable': params.commercial_data.gst_applicable,
                    'gst_percentage': params.commercial_data.gst_percentage,
                    'security_deposit_months': params.commercial_data.security_deposit_months,
                    'lease_type': params.commercial_data.lease_type,
                    'lease_tenure_years': params.commercial_data.lease_tenure_years,
                    'lock_in_period_months': params.commercial_data.lock_in_period_months,
                    'allowed_business': params.commercial_data.allowed_business,
                    'prohibited_business': params.commercial_data.prohibited_business,
                    'maintenance_charge_amount': params.commercial_data.maintenance_charge_amount,
                    'electricity_charge_amount': params.commercial_data.electricity_charge_amount,
                    'water_charge_amount': params.commercial_data.water_charge_amount,
                })
            elif params.rental_type == 'Villa' and params.villa_data:
                property_detail_kwargs.update({
                    'villa_name': params.villa_data.villa_name,
                    'villa_type': params.villa_data.villa_type,
                    'villa_configuration': params.villa_data.villa_configuration,
                    'project_name': params.villa_data.project_name,
                    'plot_area_sqft': params.villa_data.plot_area_sqft,
                    'number_of_bedrooms': params.villa_data.number_of_bedrooms,
                    'number_of_bathrooms': params.villa_data.number_of_bathrooms,
                    'living_rooms_count': params.villa_data.living_rooms_count,
                    'servant_room': params.villa_data.servant_room,
                    'balcony_or_sitout': params.villa_data.balcony_or_sitout,
                    'private_garden': params.villa_data.private_garden,
                    'terrace_access': params.villa_data.terrace_access,
                    'boundary_wall': params.villa_data.boundary_wall,
                    'driveway': params.villa_data.driveway,
                    'private_parking': params.villa_data.private_parking,
                    'villa_maintenance_charge_type': params.villa_data.villa_maintenance_charge_type,
                    'gardening_charges': params.villa_data.gardening_charges,
                    'water_supply_24x7': params.villa_data.water_supply_24x7,
                    'security_guard': params.villa_data.security_guard,
                    'clubhouse_access': params.villa_data.clubhouse_access,
                    'gym': params.villa_data.gym,
                    'childrens_play_area': params.villa_data.childrens_play_area,
                    'internal_roads': params.villa_data.internal_roads,
                    'street_lights': params.villa_data.street_lights,
                    'gated_community': params.villa_data.gated_community,
                    'bachelor_allowed': params.villa_data.bachelor_allowed,
                    'pets_allowed': params.villa_data.pets_allowed,
                    'power_backup': params.villa_data.power_backup,
                    'cctv': params.villa_data.cctv,
                    'allowed_tenant_types': params.villa_data.allowed_tenant_types,
                    'store_room': params.villa_data.store_room,
                    'maintenance_charge_amount': params.villa_data.maintenance_charge_amount,
                    'electricity_charge_amount': params.villa_data.electricity_charge_amount,
                    'water_charge_amount': params.villa_data.water_charge_amount,
                })

            PropertyDetail.create(**property_detail_kwargs)

            if params.photos:
                from pms_apps.property.models.property_photos import PropertyPhotos
                from pms_apps.property.image_utils import ImageUtils
                
                for photo_data in params.photos:
                    # Process the photo (convert base64 to file or use URL as-is)
                    processed_photo = ImageUtils.process_photo(photo_data)
                    if processed_photo:
                        if isinstance(processed_photo, tuple) and processed_photo[0] == 'url':
                            # It's a URL, store the URL string directly
                            photo_obj = PropertyPhotos.objects.create(
                                property_id=property_id
                            )
                            photo_obj.photo = processed_photo[1]
                            photo_obj.save()
                        else:
                            # It's a ContentFile object, save it
                            photo_obj = PropertyPhotos.objects.create(
                                property_id=property_id
                            )
                            photo_obj.photo.save(
                                processed_photo.name,
                                processed_photo,
                                save=True
                            )

        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(message=self.data_create, data={'property_id': property_id})
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
        

        with transaction.atomic():
            Property.update(
                property_id=params.property_id,
                block=params.block,
                building_details=params.building_details,
                floor=params.floor,
                flat_number=params.flat_number,
                dimension_length_ft=params.dimension_length_ft,
                dimension_breadth_ft=params.dimension_breadth_ft,
                dimension_area_sqft=params.dimension_area_sqft,
                rental_type=params.rental_type,
                rental_for=params.rental_for,
                advance_amount_rent=params.advance_amount_rent,
                expected_rent=params.expected_rent,
                agreement_id=params.agreement_id,
                assigned_to=assigned_to_user.get('user_id') if assigned_to_user else None,
            )

           
            
            detail_update_kwargs = {}
            if params.property_details:
                detail_update_kwargs.update({k: v for k, v in params.property_details.__dict__.items() if v is not None})
            
            rental_type = params.rental_type or property_obj.get('rental_type')
            
            if rental_type == 'Flat' and params.flat_data:
                detail_update_kwargs.update({k: v for k, v in params.flat_data.__dict__.items() if v is not None})
            elif rental_type == 'Commercial' and params.commercial_data:
                detail_update_kwargs.update({k: v for k, v in params.commercial_data.__dict__.items() if v is not None})
            elif rental_type == 'Villa' and params.villa_data:
                detail_update_kwargs.update({k: v for k, v in params.villa_data.__dict__.items() if v is not None})
            
            if detail_update_kwargs:
                PropertyDetail.update(property_id=params.property_id, **detail_update_kwargs)

            if params.photos:
                from pms_apps.property.models.property_photos import PropertyPhotos
                from pms_apps.property.image_utils import ImageUtils
                
                # Delete existing photos
                PropertyPhotos.objects.filter(property_id=params.property_id).delete()
                
                # Add new photos
                for photo_data in params.photos:
                    # Process the photo (convert base64 to file or use URL as-is)
                    processed_photo = ImageUtils.process_photo(photo_data)
                    if processed_photo:
                        if isinstance(processed_photo, tuple) and processed_photo[0] == 'url':
                            # It's a URL, store the URL string directly
                            photo_obj = PropertyPhotos.objects.create(
                                property_id=params.property_id
                            )
                            photo_obj.photo = processed_photo[1]
                            photo_obj.save()
                        else:
                            # It's a ContentFile object, save it
                            photo_obj = PropertyPhotos.objects.create(
                                property_id=params.property_id
                            )
                            photo_obj.photo.save(
                                processed_photo.name,
                                processed_photo,
                                save=True
                            )
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_update)
        )


    def _categorize_property_details(self, property_dict, detail_dict, rental_type):
        """Helper to structure detail_dict into categorized fields within property_dict."""
        # Common details
        common_fields = [
            'property_code', 'building_name', 'total_floors', 'carpet_area_sqft', 'builtup_area_sqft',
            'monthly_rent', 'security_deposit_amount', 'electricity_charge_type',
            'water_charge_type', 'late_fee_type', 'late_fee_value', 'current_status',
            'landlord_id', 'address_line_1', 'address_line_2', 'area_zone', 'city',
            'state', 'country', 'pincode', 'google_map_location', 'year_of_construction',
            'other_charges', 'available_from', 'current_tenant_id', 'internal_notes'
        ]
        property_dict['propertyDetails'] = {k: detail_dict.get(k) for k in common_fields if k in detail_dict}
        
        # Type specific details
        if rental_type == 'Flat':
            flat_fields = [
                'flat_number', 'floor_number', 'building_block', 'flat_configuration',
                'no_of_bathrooms', 'kitchen_type', 'facing', 'balcony', 'parking',
                'lift', 'security', 'gas_pipeline', 'water_supply', 'intercom',
                'fire_safety', 'power_backup', 'cctv', 'allowed_tenant_types', 'store_room',
                'maintenance_charge_amount', 'electricity_charge_amount', 'water_charge_amount'
            ]
            property_dict['flatData'] = {k: detail_dict.get(k) for k in flat_fields if k in detail_dict}
        elif rental_type == 'Commercial':
            commercial_fields = [
                'commercial_category', 'floor_number', 'frontage_width_ft', 'ceiling_height_ft',
                'no_of_cabins', 'no_of_washrooms', 'loading_area', 'power_load_kw',
                'has_dg_backup', 'lift_type', 'fire_safety_compliant', 'emergency_exit',
                'parking_availability', 'commercial_maintenance_charge_type',
                'maintenance_charge_amount', 'electricity_charge_amount', 'water_charge_amount',
                'gst_applicable', 'gst_percentage', 'security_deposit_months', 'lease_type',
                'lease_tenure_years', 'lock_in_period_months', 'allowed_business', 'prohibited_business'
            ]
            property_dict['commercialData'] = {k: detail_dict.get(k) for k in commercial_fields if k in detail_dict}
        elif rental_type == 'Villa':
            villa_fields = [
                'villa_name', 'villa_type', 'villa_configuration', 'project_name',
                'plot_area_sqft', 'number_of_bedrooms', 'number_of_bathrooms',
                'living_rooms_count', 'servant_room', 'balcony_or_sitout', 'private_garden',
                'terrace_access', 'boundary_wall', 'driveway', 'private_parking',
                'villa_maintenance_charge_type', 'gardening_charges', 'water_supply_24x7',
                'security_guard', 'clubhouse_access', 'gym', 'childrens_play_area',
                'internal_roads', 'street_lights', 'gated_community', 'bachelor_allowed',
                'pets_allowed', 'power_backup', 'cctv', 'allowed_tenant_types', 'store_room',
                'maintenance_charge_amount', 'electricity_charge_amount', 'water_charge_amount'
            ]
            property_dict['villaData'] = {k: detail_dict.get(k) for k in villa_fields if k in detail_dict}

    @Common(response_handler=PropertyResponseGetSerializer).exception_handler
    def get_extract(self, params: PropertyGetRequest):
        property_data = Property.get(property_id=params.property_id)
        if not property_data:
            raise ValueError(self.data_no_match)
        
        # Check if user has access to this property
        has_access = (
            property_data.get('created_by__user_id') == params.user_id or 
            property_data.get('assigned_to__user_id') == params.user_id
        )
        
        # Check if user is the landlord through PropertyDetail
        if not has_access:
            from pms_apps.property.models.property_details import PropertyDetail
            landlord_check = PropertyDetail.objects.filter(
                property_id=params.property_id,
                landlord__lead_id__user_id=params.user_id
            ).exists()
            has_access = landlord_check
        
        if not has_access:
            raise ValueError("Not allowed to access this resource")

        from pms_apps.property.models.property_details import PropertyDetail
        from django.forms.models import model_to_dict
        
        detail_obj = PropertyDetail.get_by_property(property_id=params.property_id)
        detail_dict = model_to_dict(detail_obj) if detail_obj else {}

        utils = PropertyUtils(columns_required=[column for column in params.values.split(',') if column])
        property_dict = json.loads(utils.mapper([property_data]))[0]
        
        self._categorize_property_details(property_dict, detail_dict, property_data.get('rental_type'))

        # Add photos
        from pms_apps.property.models.property_photos import PropertyPhotos
        from pms_apps.property.image_utils import ImageUtils
        
        photos = PropertyPhotos.objects.filter(property_id=params.property_id)
        photos_urls = []
        for photo in photos:
            if photo.photo:
                # Try to get URL - works for files. For external URLs stored as strings, return as-is
                if str(photo.photo).startswith('http://') or str(photo.photo).startswith('https://'):
                    photos_urls.append(str(photo.photo))
                else:
                    # It's a file path managed by Django
                    photos_urls.append(ImageUtils.get_photo_url(str(photo.photo)))
        property_dict['photos'] = photos_urls

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

        property_list = Property.get_all_by_user(
            user_id=params.user_id,
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            filter_key=reversed_mapped.get(params.filter_key),
            filter_value=params.filter_value,
            search_key=params.search_key
        )
        
        pages = Paginator(property_list, per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)

        page_data = pages.page(params.page_num)
        utils = PropertyUtils(columns_required=[column for column in params.values.split(',') if column])
        serialized_properties = json.loads(utils.mapper(data=page_data))

        # Fetch all details and photos for properties in the current page
        property_ids = [p['property_id'] for p in page_data]
        
        from pms_apps.property.models.property_details import PropertyDetail
        from pms_apps.property.models.property_photos import PropertyPhotos
        from pms_apps.property.image_utils import ImageUtils
        from django.forms.models import model_to_dict
        
        details_map = {d.property_id: {**model_to_dict(d), 'landlord_id': d.landlord_id, 'current_tenant_id': d.current_tenant_id} for d in PropertyDetail.get_by_properties(property_ids)}
        
        from collections import defaultdict
        photos_map = defaultdict(list)
        for photo in PropertyPhotos.objects.filter(property_id__in=property_ids):
            # Return photo URL path, not the file object
            if photo.photo:
                photo_value = str(photo.photo)
                # Check if it's already a URL
                if photo_value.startswith('http://') or photo_value.startswith('https://'):
                    photos_map[photo.property_id].append(photo_value)
                else:
                    # It's a file path managed by Django
                    photo_url = ImageUtils.get_photo_url(photo_value)
                    if photo_url:
                        photos_map[photo.property_id].append(photo_url)

        for property_dict in serialized_properties:
            pid = property_dict.get('propertyId')
            # Categorize details
            detail_dict = details_map.get(pid, {})
            self._categorize_property_details(property_dict, detail_dict, property_dict.get('rentalType'))
            # Add photos
            property_dict['photos'] = photos_map.get(pid, [])

        final_data = Utils.add_page_parameter(
            final_data=serialized_properties,
            page_num=params.page_num,
            total_page=pages.num_pages,
            present_url=params.present_url,
            next_page_required=True if pages.num_pages != params.page_num else False
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=final_data)
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

    @Common().exception_handler
    def count_extract(self, params: GetAll):
        reversed_mapped = PropertyUtils.reverse_mapper([
            params.sort_by,
            params.filter_key
        ])

        property_list = Property.get_all_by_user(
            user_id=params.user_id,
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            filter_key=reversed_mapped.get(params.filter_key),
            filter_value=params.filter_value,
            search_key=params.search_key
        )

        property_count = len(property_list)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message="Total properties count", data={"count": property_count})
        )

    @Common().exception_handler
    def assign_extract(self, params: PropertyAssignmentCreateRequest):
        from pms_apps.lead.models.lead import Lead
        
        # Validate property detail exists
        property_detail = PropertyDetail.objects.filter(property_detail_id=params.property_id).first()
        if not property_detail:
            raise ValueError(self.data_no_match)
        
        # Validate tenant exists
        try:
            tenant = Lead.objects.get(lead_id=params.tenant_id)
        except Lead.DoesNotExist:
            raise ValueError(f"Invalid Tenant ID: {params.tenant_id}")
        
        with transaction.atomic():
            # Create PropertyAssignment record
            assignment_id = PropertyAssignment.create(
                property_id=property_detail.property_id,
                tenant_id=params.tenant_id,
                assigned_by_id=params.assigned_by_id,
                assignment_status=params.assignment_status,
                tenant_type=params.tenant_type,
                company_name=params.company_name,
                rental_start_date=params.rental_start_date,
                rental_end_date=params.rental_end_date,
                agreement_duration_months=params.agreement_duration_months,
                maintenance_charges=params.maintenance_charges,
                advance_rent_paid=params.advance_rent_paid,
                payment_mode=params.payment_mode,
                agreement_type=params.agreement_type,
                agreement_status=params.agreement_status,
                agreement_prepared_by_id=params.agreement_prepared_by_id,
                key_available_in_office=params.key_available_in_office,
                key_code=params.key_code,
                key_handover_date=params.key_handover_date,
                key_handover_status=params.key_handover_status,
                electricity_meter_number=params.electricity_meter_number,
                electricity_meter_reading_start=params.electricity_meter_reading_start,
                water_meter_reading_start=params.water_meter_reading_start,
                gas_meter_reading_start=params.gas_meter_reading_start,
                finance_approval_status=params.finance_approval_status,
                rent_entry_created=params.rent_entry_created,
                invoice_generated=params.invoice_generated,
                maintenance_required=params.maintenance_required,
                maintenance_ticket_id=params.maintenance_ticket_id,
                maintenance_status=params.maintenance_status,
                internal_notes=params.internal_notes,
                tenant_special_requirements=params.tenant_special_requirements,
            )
            
            # Update PropertyDetail with current tenant and status
            property_detail.current_tenant_id = params.tenant_id
            property_detail.current_status = "Occupied"
            property_detail.save()
        
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_assign,
                data={"property_assignment_id": assignment_id}
            )
        )

    @Common().exception_handler
    def get_extract_assignment(self, params):
        """Fetch a single property assignment by ID"""
        assignment = PropertyAssignment.objects.filter(
            property_assignment_id=params.property_assignment_id,
            is_active=True
        ).first()
        
        if not assignment:
            raise ValueError(self.data_no_match)
        
        # Build response data with camelCase field names
        assignment_data = {
            "assignmentId": assignment.property_assignment_id,
            "property": {
                "propertyId": assignment.property.property_id,
                "block": assignment.property.block,
                "buildingDetails": assignment.property.building_details,
                "floor": assignment.property.floor,
                "flatNumber": assignment.property.flat_number,
            },
            "tenant": {
                "tenantId": assignment.tenant.lead_id if assignment.tenant else None,
                "firstName": assignment.tenant.lead_id.user_id.first_name if assignment.tenant and assignment.tenant.lead_id else None,
                "lastName": assignment.tenant.lead_id.user_id.last_name if assignment.tenant and assignment.tenant.lead_id else None,
                "phoneNumber": assignment.tenant.lead_id.user_id.phone_number if assignment.tenant and assignment.tenant.lead_id else None,
                "email": assignment.tenant.lead_id.user_id.email if assignment.tenant and assignment.tenant.lead_id else None,
            } if assignment.tenant else None,
            "assignedBy": {
                "userId": assignment.assigned_by.user_id if assignment.assigned_by else None,
                "phoneNumber": assignment.assigned_by.phone_number if assignment.assigned_by else None,
                "name": assignment.assigned_by.get_full_name() if assignment.assigned_by else None,
                "email": assignment.assigned_by.email if assignment.assigned_by else None,
            } if assignment.assigned_by else None,
            "assignmentStatus": assignment.assignment_status,
            "tenantType": assignment.tenant_type,
            "companyName": assignment.company_name,
            "rentalStartDate": assignment.rental_start_date,
            "rentalEndDate": assignment.rental_end_date,
            "agreementDurationMonths": assignment.agreement_duration_months,
            "maintenanceCharges": str(assignment.maintenance_charges) if assignment.maintenance_charges else None,
            "advanceRentPaid": assignment.advance_rent_paid,
            "paymentMode": assignment.payment_mode,
            "agreementType": assignment.agreement_type,
            "agreementStatus": assignment.agreement_status,
            "keyAvailableInOffice": assignment.key_available_in_office,
            "keyCode": assignment.key_code,
            "keyHandoverDate": assignment.key_handover_date,
            "keyHandoverStatus": assignment.key_handover_status,
            "electricityMeterNumber": assignment.electricity_meter_number,
            "electricityMeterReadingStart": str(assignment.electricity_meter_reading_start) if assignment.electricity_meter_reading_start else None,
            "waterMeterReadingStart": str(assignment.water_meter_reading_start) if assignment.water_meter_reading_start else None,
            "gasMeterReadingStart": str(assignment.gas_meter_reading_start) if assignment.gas_meter_reading_start else None,
            "financeApprovalStatus": assignment.finance_approval_status,
            "rentEntryCreated": assignment.rent_entry_created,
            "invoiceGenerated": assignment.invoice_generated,
            "maintenanceRequired": assignment.maintenance_required,
            "maintenanceTicketId": assignment.maintenance_ticket_id,
            "maintenanceStatus": assignment.maintenance_status,
            "internalNotes": assignment.internal_notes,
            "tenantSpecialRequirements": assignment.tenant_special_requirements,
            "assignedOn": assignment.assigned_on,
            "unassignedOn": assignment.unassigned_on,
            "createdAt": assignment.created_at,
            "updatedAt": assignment.updated_at,
        }
        
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_get,
                data=assignment_data
            )
        )

    @Common().exception_handler
    def get_all_extract_assignment(self, params: GetAll):
        """Fetch all property assignments with filtering and pagination"""
        # Base queryset
        query = PropertyAssignment.objects.filter(is_active=True).select_related(
            'property', 'tenant', 'assigned_by', 'agreement_prepared_by'
        )
        
        # Apply filters if provided
        if hasattr(params, 'filters') and params.filters:
            filters = params.filters
            if 'property_id' in filters:
                query = query.filter(property_id=filters['property_id'])
            if 'tenant_id' in filters:
                query = query.filter(tenant_id=filters['tenant_id'])
            if 'assignment_status' in filters:
                query = query.filter(assignment_status=filters['assignment_status'])
            if 'assigned_by_id' in filters:
                query = query.filter(assigned_by_id=filters['assigned_by_id'])
        
        # Apply search if provided
        if hasattr(params, 'search') and params.search:
            query = query.filter(
                Q(property__block__icontains=params.search) |
                Q(property__building_details__icontains=params.search) |
                Q(tenant__lead_id__user_id__first_name__icontains=params.search) |
                Q(tenant__lead_id__user_id__last_name__icontains=params.search)
            )
        
        # Get total count before pagination
        total_items = query.count()
        paginator = Paginator(query, Constants.PAGINATE_BY)
        
        # Validate page number
        page_num = getattr(params, 'page_num', 1)
        if page_num < 1:
            page_num = 1
        
        try:
            assignments = paginator.page(page_num).object_list
        except Exception:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=Utils.error_response_data(message="Invalid page number")
            )
        
        # Build response data
        assignments_data = []
        for assignment in assignments:
            assignment_item = {
                "assignmentId": assignment.property_assignment_id,
                "property": {
                    "propertyId": assignment.property.property_id,
                    "block": assignment.property.block,
                    "buildingDetails": assignment.property.building_details,
                    "floor": assignment.property.floor,
                    "flatNumber": assignment.property.flat_number,
                },
                "tenant": {
                    "tenantId": assignment.tenant.lead_id if assignment.tenant else None,
                    "firstName": assignment.tenant.lead_id.user_id.first_name if assignment.tenant and assignment.tenant.lead_id else None,
                    "lastName": assignment.tenant.lead_id.user_id.last_name if assignment.tenant and assignment.tenant.lead_id else None,
                    "phoneNumber": assignment.tenant.lead_id.user_id.phone_number if assignment.tenant and assignment.tenant.lead_id else None,
                    "email": assignment.tenant.lead_id.user_id.email if assignment.tenant and assignment.tenant.lead_id else None,
                } if assignment.tenant else None,
                "assignementStatus": assignment.assignment_status,
                "rentalStartDate": assignment.rental_start_date,
                "rentalEndDate": assignment.rental_end_date,
                "assignedOn": assignment.assigned_on,
            }
            assignments_data.append(assignment_item)
        
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_get,
                data={
                    "data": assignments_data,
                    "presentPage": page_num,
                    "totalPage": paginator.num_pages,
                }
            )
        )
