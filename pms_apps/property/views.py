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
from pms_apps.property.dataclasses.requests.get_all_property import PropertyGetAllRequest
from pms_apps.property.dataclasses.requests.property_assignment_create import PropertyAssignmentCreateRequest
from pms_apps.property.dataclasses.requests.property_assignment_update import PropertyAssignmentUpdateRequest
from pms_apps.property.dataclasses.requests.occupancy_report import OccupancyReportRequest
from pms_apps.property.dataclasses.requests.rental_report import RentalReportRequest
from pms_apps.property.utils import PropertyUtils

from pms_apps.property.models.property import Property
from pms_apps.property.serializers.response.get import PropertyResponseGetSerializer
from pms_apps.property.serializers.response.get_all import PropertyResponseGetAllSerializer
from pms_apps.property.serializers.response.assignment_get import PropertyAssignmentResponseGetSerializer
from pms_apps.property.serializers.response.assignment_get_all import PropertyAssignmentResponseGetAllSerializer

from pms_apps.property.models.property_details import PropertyDetail
from pms_apps.property.models.property_assignment import PropertyAssignment
from pms_apps.marketing.models.marketing_manager import MarketingManager


def _percentage(part: int, total: int) -> float:
    return round((part / total) * 100, 2) if total else 0.0


def _month_over_month_change(queryset, date_field: str = "created_at") -> float:
    from datetime import date, timedelta

    today = date.today()
    this_month = queryset.filter(**{f"{date_field}__year": today.year, f"{date_field}__month": today.month}).count()
    prev_month_date = today.replace(day=1) - timedelta(days=1)
    last_month = queryset.filter(
        **{f"{date_field}__year": prev_month_date.year, f"{date_field}__month": prev_month_date.month}
    ).count()
    if last_month == 0:
        return 100.0 if this_month else 0.0
    return round(((this_month - last_month) / last_month) * 100, 2)


class PropertyView:
    def __init__(self) -> None:
        super().__init__()
        self.data_create = "Property added successfully"
        self.data_update = "Property updated successfully"
        self.data_delete = "Property deleted successfully"
        self.data_get = "Property fetched successfully"
        self.data_no_match = "No matching property found"
        self.data_assign = "Property assigned to tenant successfully"
        self.data_occupancy_summary = "Occupancy summary fetched successfully"
        self.data_occupancy_list = "Occupancy report fetched successfully"
        self.data_rental_report_summary = "Rental report summary fetched successfully"
        self.data_rental_report_list = "Rental report fetched successfully"
        self.data_assignment_count = "Assignment count fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common().exception_handler
    def create_extract(self, params: PropertyCreateRequest):
        PropertyUtils.check_constraints(params=params)

        building_data = None
        if params.building_id:
            from pms_apps.property.models.building import Building
            building_data = Building.get(building_id=params.building_id)
            if not building_data:
                raise ValueError(f"Invalid Building Id: {params.building_id}")
            building_property_type = building_data.get('property_type')
            if building_property_type and building_property_type != params.rental_type:
                raise ValueError(
                    f"Building '{building_data.get('name')}' only accepts '{building_property_type}' "
                    f"units, but '{params.rental_type}' was requested."
                )

        def _from_building(key):
            return building_data.get(key) if building_data else None

        # Mirror nested data to root Property fields for cleaner visibility
        block = params.block or params.property_details.address_line_2
        building_details = params.building_details or params.property_details.building_name or _from_building('name')
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
                building_id=params.building_id,
            )

            from pms_apps.property.models.property_details import PropertyDetail

            property_detail_kwargs = {
                'property_id': property_id,
                'building_name': params.property_details.building_name or _from_building('name'),
                'unit_number': params.property_details.unit_number,
                'rental_purpose': params.property_details.rental_purpose,
                'total_floors': params.property_details.total_floors,
                'carpet_area_sqft': params.property_details.carpet_area_sqft,
                'builtup_area_sqft': params.property_details.builtup_area_sqft,
                'monthly_rent': params.property_details.monthly_rent,
                'security_deposit_amount': params.property_details.security_deposit_amount,
                'electricity_charge_type': params.property_details.electricity_charge_type or None,
                'water_charge_type': params.property_details.water_charge_type or None,
                'late_fee_type': params.property_details.late_fee_type,
                'late_fee_value': params.property_details.late_fee_value,
                'current_status': params.property_details.current_status,
                'landlord_id': params.property_details.landlord_id,
                'created_by_id': params.user_id or params.property_details.created_by_id,
                'address_line_1': params.property_details.address_line_1 or _from_building('address_line_1'),
                'area_zone': params.property_details.area_zone or _from_building('area_zone'),
                'city': params.property_details.city or _from_building('city'),
                'state': params.property_details.state or _from_building('state'),
                'country': params.property_details.country or _from_building('country'),
                'pincode': params.property_details.pincode or _from_building('pincode'),
                'google_map_location': params.property_details.google_map_location or _from_building('google_map_location'),
                'year_of_construction': params.property_details.year_of_construction,
                'other_charges': params.property_details.other_charges,
                'available_from': params.property_details.available_from,
                'current_tenant_id': params.property_details.current_tenant_id,
                'address_line_2': params.property_details.address_line_2,
                'internal_notes': params.property_details.internal_notes,
                'furnishing_status': params.property_details.furnishing_status,
                'payment_due_date': params.property_details.payment_due_date,
                'rent_increase_date': params.property_details.rent_increase_date,
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
                    'cctv': params.commercial_data.cctv,
                    'super_builtup_area_sqft': params.commercial_data.super_builtup_area_sqft,
                    'pantry': params.commercial_data.pantry,
                    'store_room': params.commercial_data.store_room,
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
                    'facing': params.villa_data.facing,
                    'kitchen_type': params.villa_data.kitchen_type,
                    'swimming_pool': params.villa_data.swimming_pool,
                    'unit': params.villa_data.unit,
                    'super_builtup_area_sqft': params.villa_data.super_builtup_area_sqft,
                    'pantry': params.villa_data.pantry,
                })
            elif params.rental_type == 'Warehouse' and params.warehouse_data:
                property_detail_kwargs.update({
                    'warehouse_category': params.warehouse_data.warehouse_category,
                    'warehouse_name': params.warehouse_data.warehouse_name,
                    'industrial_estate_name': params.warehouse_data.industrial_estate_name,
                    'plot_shed_number': params.warehouse_data.plot_shed_number,
                    'ownership_type': params.warehouse_data.ownership_type,
                    'clear_height_ft': params.warehouse_data.clear_height_ft,
                    'no_of_bays': params.warehouse_data.no_of_bays,
                    'no_of_loading_docks': params.warehouse_data.no_of_loading_docks,
                    'dock_height_ft': params.warehouse_data.dock_height_ft,
                    'floor_load_capacity_mt_sqft': params.warehouse_data.floor_load_capacity_mt_sqft,
                    'column_spacing_ft': params.warehouse_data.column_spacing_ft,
                    'has_mezzanine_floor': params.warehouse_data.has_mezzanine_floor,
                    'office_space_area_sqft': params.warehouse_data.office_space_area_sqft,
                    'has_transformer': params.warehouse_data.has_transformer,
                    'water_supply_source': params.warehouse_data.water_supply_source,
                    'has_drainage_system': params.warehouse_data.has_drainage_system,
                    'has_internet_fiber': params.warehouse_data.has_internet_fiber,
                    'entry_gate_width_ft': params.warehouse_data.entry_gate_width_ft,
                    'road_width_ft': params.warehouse_data.road_width_ft,
                    'truck_parking_capacity': params.warehouse_data.truck_parking_capacity,
                    'container_access': params.warehouse_data.container_access,
                    'turning_radius': params.warehouse_data.turning_radius,
                    'has_weighbridge_nearby': params.warehouse_data.has_weighbridge_nearby,
                    'monthly_rent_type': params.warehouse_data.monthly_rent_type,
                    'rent_escalation_percentage': params.warehouse_data.rent_escalation_percentage,
                    'lock_in_period_months': params.warehouse_data.lock_in_period_months,
                    'allowed_industry_types': params.warehouse_data.allowed_industry_types,
                    'maintenance_charges': params.warehouse_data.maintenance_charges,
                    'cam_charges': params.warehouse_data.cam_charges,
                    'security_deposit_type': params.warehouse_data.security_deposit_type,
                    'security_deposit_months': params.warehouse_data.security_deposit_months,
                    'has_dg_backup': params.warehouse_data.has_dg_backup,
                    'power_load_kw': params.warehouse_data.power_load_kw,
                    'plot_area_sqft': params.warehouse_data.plot_area_sqft,
                    'loading_area': params.warehouse_data.loading_area,
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

        property_obj = Property.get(property_id=params.property_id)
        if not property_obj:
            raise ValueError(self.data_no_match)

        new_building_data = None
        if params.building_id:
            from pms_apps.property.models.building import Building
            new_building_data = Building.get(building_id=params.building_id)
            if not new_building_data:
                raise ValueError(f"Invalid Building Id: {params.building_id}")

        # Enforce the building's property_type lock against whichever building/
        # rental_type is in effect after this update (either could be unchanged).
        effective_rental_type = params.rental_type or property_obj.get('rental_type')
        effective_building_data = new_building_data
        if effective_building_data is None and property_obj.get('building_id'):
            from pms_apps.property.models.building import Building
            effective_building_data = Building.get(building_id=property_obj.get('building_id'))
        if effective_building_data:
            building_property_type = effective_building_data.get('property_type')
            if building_property_type and building_property_type != effective_rental_type:
                raise ValueError(
                    f"Building '{effective_building_data.get('name')}' only accepts "
                    f"'{building_property_type}' units, but '{effective_rental_type}' was requested."
                )

        with transaction.atomic():
            Property.update(
                property_id=params.property_id,
                block=params.block,
                building_details=params.building_details or (new_building_data.get('name') if new_building_data else None),
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
                assigned_to=params.assigned_to,
                building_id=params.building_id,
            )



            detail_update_kwargs = {}
            if params.property_details:
                detail_update_kwargs.update({k: v for k, v in params.property_details.__dict__.items() if v is not None})

            # Moving a unit to a different building refreshes the denormalized
            # building_name unless the caller explicitly set one on this call.
            if new_building_data and 'building_name' not in detail_update_kwargs:
                detail_update_kwargs['building_name'] = new_building_data.get('name')
            
            rental_type = params.rental_type or property_obj.get('rental_type')
            
            if rental_type == 'Flat' and params.flat_data:
                detail_update_kwargs.update({k: v for k, v in params.flat_data.__dict__.items() if v is not None})
            elif rental_type == 'Commercial' and params.commercial_data:
                detail_update_kwargs.update({k: v for k, v in params.commercial_data.__dict__.items() if v is not None})
            elif rental_type == 'Villa' and params.villa_data:
                detail_update_kwargs.update({k: v for k, v in params.villa_data.__dict__.items() if v is not None})
            
            if detail_update_kwargs:
                PropertyDetail.update(property_id=params.property_id, **detail_update_kwargs)

            if params.photos is not None:
                from pms_apps.property.models.property_photos import PropertyPhotos
                from pms_apps.property.image_utils import ImageUtils

                # `photos` is the full desired photo list: existing photos are represented
                # by the URLs the GET endpoint returns, new uploads by base64 strings.
                # Any existing photo whose URL is missing from this list was removed by
                # the client and must be deleted (file + row), not just left orphaned.
                existing_photos = list(PropertyPhotos.objects.filter(property_id=params.property_id))
                existing_by_url = {}
                for photo_obj in existing_photos:
                    if not photo_obj.photo:
                        continue
                    photo_str = str(photo_obj.photo)
                    url = photo_str if photo_str.startswith(('http://', 'https://')) else ImageUtils.get_photo_url(photo_str)
                    if url:
                        existing_by_url[url] = photo_obj

                submitted_set = set(params.photos)

                # Delete photos removed by the client (their URL is no longer submitted)
                for url, photo_obj in existing_by_url.items():
                    if url not in submitted_set:
                        photo_obj.photo.delete(save=False)
                        photo_obj.delete()

                # Add photos that aren't references to an already-kept existing photo
                for photo_data in params.photos:
                    if photo_data in existing_by_url:
                        continue

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


    def _to_camel_case(self, snake_str: str) -> str:
        """Convert snake_case to camelCase"""
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def _categorize_property_details(self, property_dict, detail_dict, rental_type):
        """Helper to structure detail_dict into categorized fields within property_dict."""
        # Common details
        common_fields = [
            'property_code', 'building_name', 'unit_number', 'rental_purpose', 'total_floors', 'carpet_area_sqft', 'builtup_area_sqft',
            'monthly_rent', 'security_deposit_amount', 'electricity_charge_type',
            'water_charge_type', 'late_fee_type', 'late_fee_value', 'current_status',
            'landlord_id', 'address_line_1', 'address_line_2', 'area_zone', 'city',
            'state', 'country', 'pincode', 'google_map_location', 'year_of_construction',
            'other_charges', 'available_from', 'current_tenant_id', 'internal_notes',
            'furnishing_status', 'payment_due_date', 'rent_increase_date'
        ]
        property_dict['propertyDetails'] = {
            self._to_camel_case(k): detail_dict.get(k) 
            for k in common_fields if k in detail_dict
        }
        
        # Type specific details
        if rental_type == 'Flat':
            flat_fields = [
                'flat_number', 'floor_number', 'building_block', 'flat_configuration',
                'no_of_bathrooms', 'kitchen_type', 'facing', 'balcony', 'parking',
                'lift', 'security', 'gas_pipeline', 'water_supply', 'intercom',
                'fire_safety', 'power_backup', 'cctv', 'allowed_tenant_types', 'store_room',
                'maintenance_charge_amount', 'electricity_charge_amount', 'water_charge_amount'
            ]
            property_dict['flatData'] = {self._to_camel_case(k): detail_dict.get(k) for k in flat_fields if k in detail_dict}
        elif rental_type == 'Commercial':
            commercial_fields = [
                'commercial_category', 'floor_number', 'frontage_width_ft', 'ceiling_height_ft',
                'no_of_cabins', 'no_of_washrooms', 'loading_area', 'power_load_kw',
                'has_dg_backup', 'lift_type', 'fire_safety_compliant', 'emergency_exit',
                'parking_availability', 'commercial_maintenance_charge_type',
                'maintenance_charge_amount', 'electricity_charge_amount', 'water_charge_amount',
                'gst_applicable', 'gst_percentage', 'security_deposit_months', 'lease_type',
                'lease_tenure_years', 'lock_in_period_months', 'allowed_business', 'prohibited_business',
                'pantry', 'store_room'
            ]
            property_dict['commercialData'] = {self._to_camel_case(k): detail_dict.get(k) for k in commercial_fields if k in detail_dict}
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
            property_dict['villaData'] = {self._to_camel_case(k): detail_dict.get(k) for k in villa_fields if k in detail_dict}

    @Common(response_handler=PropertyResponseGetSerializer).exception_handler
    def get_extract(self, params: PropertyGetRequest):
        property_data = Property.get(property_id=params.property_id)
        if not property_data:
            raise ValueError(self.data_no_match)
        
        # Check if user has access to this property
        is_assigned = Property.objects.filter(
            property_id=params.property_id,
            assigned_to__user_id=params.user_id
        ).exists()
        has_access = (
            property_data.get('created_by__user_id') == params.user_id or
            is_assigned
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
        property_dict['assignedTo'] = Property.get_assignees_map([params.property_id]).get(params.property_id, [])

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=property_dict)
        )

    @Common(response_handler=PropertyResponseGetAllSerializer).exception_handler
    def get_all_extract(self, params: PropertyGetAllRequest):
        reversed_mapped = PropertyUtils.reverse_mapper([params.sort_by])

        property_list = Property.get_all_by_user(
            user_id=params.user_id,
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            search_key=params.search_key,
            property_types=params.property_types,
            rental_for=params.rental_for,
            bedrooms=params.bedrooms,
            features=params.features,
            building_id=params.building_id,
            city=params.city,
            min_rent=params.min_rent,
            max_rent=params.max_rent,
            from_date=params.from_date,
            to_date=params.to_date,
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
        
        details_map = {d.property_id: {**model_to_dict(d), 'landlord_id': d.landlord_id, 'current_tenant_id': d.current_tenant} for d in PropertyDetail.get_by_properties(property_ids)}
        
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

        assignees_map = Property.get_assignees_map(property_ids)

        for property_dict in serialized_properties:
            pid = property_dict.get('propertyId')
            # Categorize details
            detail_dict = details_map.get(pid, {})
            self._categorize_property_details(property_dict, detail_dict, property_dict.get('rentalType'))
            # Add photos
            property_dict['photos'] = photos_map.get(pid, [])
            # Add assigned users
            property_dict['assignedTo'] = assignees_map.get(pid, [])

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
        from django.db.models import Count

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

        # Count by property type (rental_type), keeping every known type in the
        # response even when its count is 0 so the frontend has a stable shape.
        by_type = {choice: 0 for choice, _ in Property.RENTAL_TYPE_CHOICES}
        for prop in property_list:
            rental_type = prop.get('rental_type')
            if rental_type in by_type:
                by_type[rental_type] += 1

        # Count by country (lives on PropertyDetail, not Property, so needs its own query)
        property_ids = [prop['property_id'] for prop in property_list]
        by_country = {}
        if property_ids:
            country_rows = PropertyDetail.objects.filter(
                property_id__in=property_ids
            ).values('country').annotate(count=Count('country'))
            for row in country_rows:
                by_country[row['country'] or 'Unknown'] = row['count']

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Total properties count",
                data={
                    "count": property_count,
                    "byType": by_type,
                    "byCountry": by_country,
                }
            )
        )

    @Common().exception_handler
    def occupancy_summary_extract(self, params: GetAll):
        from django.db.models import Count

        detail_query = PropertyDetail.objects.filter(property__is_active=True)
        total_properties = detail_query.count()

        status_counts = dict(
            detail_query.values("current_status").annotate(count=Count("property_detail_id"))
            .values_list("current_status", "count")
        )
        rented = status_counts.get("Occupied", 0)
        vacant = status_counts.get("Vacant", 0)
        booked = status_counts.get("Booked", 0)

        rented_change_percentage = _month_over_month_change(
            detail_query.filter(current_status="Occupied"), date_field="updated_at"
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_occupancy_summary,
                data={
                    "totalProperties": total_properties,
                    "rented": rented,
                    "rentedChangePercentage": rented_change_percentage,
                    "vacant": vacant,
                    "booked": booked,
                }
            )
        )

    @Common().exception_handler
    def occupancy_list_extract(self, params: OccupancyReportRequest):
        from pms_apps.checkin_checkout.models.check_in import CheckIn
        from pms_apps.property.models.property_assignment import PropertyAssignment

        TYPE_DISPLAY_ALIAS = {"Flat": "Apartment"}
        TYPE_ALIAS_TO_DB = {"Apartment": "Flat"}
        STATUS_DISPLAY_ALIAS = {"Occupied": "Rented"}
        STATUS_ALIAS_TO_DB = {"Rented": "Occupied"}

        query = Property.objects.filter(is_active=True)

        if params.property_types:
            db_types = [TYPE_ALIAS_TO_DB.get(t, t) for t in params.property_types]
            query = query.filter(rental_type__in=db_types)

        if params.statuses:
            db_statuses = [STATUS_ALIAS_TO_DB.get(s, s) for s in params.statuses]
            query = query.filter(propertydetail__current_status__in=db_statuses)

        if params.search:
            search_filter = (
                Q(building_details__icontains=params.search) |
                Q(propertydetail__building_name__icontains=params.search) |
                Q(propertydetail__flat_number__icontains=params.search) |
                Q(propertydetail__villa_name__icontains=params.search) |
                Q(propertydetail__warehouse_name__icontains=params.search) |
                Q(propertydetail__commercial_category__icontains=params.search)
            )
            if params.search.isdigit():
                search_filter |= Q(property_id=int(params.search))
            query = query.filter(search_filter)

        rows = list(query.values(
            "property_id", "rental_type"
        ).distinct())
        property_ids = [row["property_id"] for row in rows]

        detail_map = {
            d["property_id"]: d
            for d in PropertyDetail.objects.filter(property_id__in=property_ids).values(
                "property_id", "building_name", "current_status",
                "flat_number", "flat_configuration",
                "villa_name", "villa_configuration",
                "warehouse_name", "plot_shed_number",
                "commercial_category",
            )
        }

        check_in_map = {}
        for ci in CheckIn.objects.filter(
            is_active=True, property_id__in=property_ids
        ).order_by("property_id", "-check_in_date").values(
            "property_id", "agreement_start_date", "agreement_end_date", "monthly_rent"
        ):
            check_in_map.setdefault(ci["property_id"], ci)

        assignment_map = {}
        for a in PropertyAssignment.objects.filter(
            is_active=True, property_id__in=property_ids
        ).exclude(assignment_status__in=["Completed", "Cancelled"]).order_by(
            "property_id", "-assigned_on"
        ).values(
            "property_id", "rental_start_date", "rental_end_date", "maintenance_charges"
        ):
            assignment_map.setdefault(a["property_id"], a)

        data_rows = []
        for row in rows:
            pid = row["property_id"]
            rental_type = row["rental_type"]
            detail = detail_map.get(pid) or {}
            display_type = TYPE_DISPLAY_ALIAS.get(rental_type, rental_type)

            if rental_type == "Flat":
                unit_no = detail.get("flat_number")
                configuration = detail.get("flat_configuration")
            elif rental_type == "Villa":
                unit_no = detail.get("villa_name")
                configuration = detail.get("villa_configuration")
            elif rental_type == "Warehouse":
                unit_no = detail.get("warehouse_name") or detail.get("plot_shed_number")
                configuration = None
            else:
                unit_no = detail.get("commercial_category")
                configuration = None

            property_name = f"{configuration} {display_type}" if configuration else display_type

            ci = check_in_map.get(pid)
            assignment = assignment_map.get(pid)
            if ci:
                start_date, end_date, rent = ci["agreement_start_date"], ci["agreement_end_date"], ci["monthly_rent"]
            elif assignment:
                start_date, end_date, rent = (
                    assignment["rental_start_date"], assignment["rental_end_date"], assignment["maintenance_charges"]
                )
            else:
                start_date, end_date, rent = None, None, None

            if params.from_date and (not start_date or start_date < params.from_date.date()):
                continue
            if params.to_date and (not start_date or start_date > params.to_date.date()):
                continue

            data_rows.append({
                "propertyId": pid,
                "propertyName": property_name,
                "type": display_type,
                "buildingProject": detail.get("building_name"),
                "unitNo": unit_no,
                "startDate": start_date,
                "endDate": end_date,
                "rent": rent,
                "status": STATUS_DISPLAY_ALIAS.get(detail.get("current_status"), detail.get("current_status")),
            })

        pages = Paginator(data_rows, per_page=params.limit)
        if pages.num_pages and pages.num_pages < params.page_num:
            raise ValueError("Page limit exceed!")
        page_data = list(pages.page(params.page_num)) if pages.num_pages else []

        data = Utils.add_page_parameter(
            final_data=page_data,
            page_num=params.page_num,
            total_page=pages.num_pages,
            present_url=params.present_url,
            next_page_required=True if pages.num_pages != params.page_num else False,
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_occupancy_list, data=data)
        )

    def _build_rental_report_rows(self, params) -> list:
        import re
        from pms_apps.checkin_checkout.models.check_in import CheckIn
        from pms_apps.property.models.property_assignment import PropertyAssignment

        TYPE_DISPLAY_ALIAS = {"Flat": "Apartment"}
        TYPE_ALIAS_TO_DB = {"Apartment": "Flat"}
        STATUS_ALIAS_TO_DB = {"Active": ["Occupied"], "Inactive": ["Vacant", "Booked", "Under Maintenance"]}
        FEATURE_FIELDS = {"Balcony": ("balcony", "balcony_or_sitout"), "Parking": ("parking",), "Pool": ("swimming_pool",)}

        query = Property.objects.filter(is_active=True)

        if params.property_types:
            db_types = [TYPE_ALIAS_TO_DB.get(t, t) for t in params.property_types]
            query = query.filter(rental_type__in=db_types)

        if params.rental_for:
            query = query.filter(rental_for__in=params.rental_for)

        if params.statuses:
            db_statuses = []
            for s in params.statuses:
                db_statuses.extend(STATUS_ALIAS_TO_DB.get(s, [s]))
            query = query.filter(propertydetail__current_status__in=db_statuses)

        if params.city:
            query = query.filter(propertydetail__city__icontains=params.city)

        if params.search:
            search_filter = (
                Q(building_details__icontains=params.search) |
                Q(propertydetail__building_name__icontains=params.search) |
                Q(propertydetail__flat_number__icontains=params.search) |
                Q(propertydetail__villa_name__icontains=params.search) |
                Q(propertydetail__warehouse_name__icontains=params.search) |
                Q(propertydetail__commercial_category__icontains=params.search)
            )
            if params.search.isdigit():
                search_filter |= Q(property_id=int(params.search))
            query = query.filter(search_filter)

        rows = list(query.values(
            "property_id", "rental_type", "rental_for", "expected_rent", "created_by__name"
        ).distinct())
        property_ids = [row["property_id"] for row in rows]

        detail_map = {
            d["property_id"]: d
            for d in PropertyDetail.objects.filter(property_id__in=property_ids).values(
                "property_id", "current_status", "builtup_area_sqft",
                "flat_configuration", "villa_configuration",
                "balcony", "balcony_or_sitout", "parking", "swimming_pool",
            )
        }

        check_in_map = {}
        for ci in CheckIn.objects.filter(
            is_active=True, property_id__in=property_ids
        ).order_by("property_id", "-check_in_date").values(
            "property_id", "agreement_start_date", "monthly_rent"
        ):
            check_in_map.setdefault(ci["property_id"], ci)

        assignment_map = {}
        for a in PropertyAssignment.objects.filter(
            is_active=True, property_id__in=property_ids
        ).exclude(assignment_status__in=["Completed", "Cancelled"]).order_by(
            "property_id", "-assigned_on"
        ).values("property_id", "rental_start_date", "maintenance_charges"):
            assignment_map.setdefault(a["property_id"], a)

        data_rows = []
        for row in rows:
            pid = row["property_id"]
            rental_type = row["rental_type"]
            detail = detail_map.get(pid) or {}
            display_type = TYPE_DISPLAY_ALIAS.get(rental_type, rental_type)

            configuration = detail.get("flat_configuration") if rental_type == "Flat" else (
                detail.get("villa_configuration") if rental_type == "Villa" else None
            )
            title = f"{configuration} {display_type}" if configuration else display_type
            rooms_match = re.match(r"^(\d+)", configuration) if configuration else None
            rooms = int(rooms_match.group(1)) if rooms_match else None

            features = []
            if detail.get("balcony") or detail.get("balcony_or_sitout"):
                features.append("Balcony")
            if detail.get("parking"):
                features.append("Parking")
            if detail.get("swimming_pool") and detail.get("swimming_pool") != "No":
                features.append("Pool")

            ci = check_in_map.get(pid)
            assignment = assignment_map.get(pid)
            if ci:
                start_date, rent = ci["agreement_start_date"], ci["monthly_rent"]
            elif assignment:
                start_date, rent = assignment["rental_start_date"], assignment["maintenance_charges"]
            else:
                start_date, rent = None, None
            if rent is None:
                rent = row["expected_rent"]

            if params.from_date and (not start_date or start_date < params.from_date.date()):
                continue
            if params.to_date and (not start_date or start_date > params.to_date.date()):
                continue
            if params.bedrooms and configuration not in params.bedrooms:
                continue
            if params.features and not (set(params.features) & set(features)):
                continue
            if params.min_rent is not None and (rent is None or rent < params.min_rent):
                continue
            if params.max_rent is not None and (rent is None or rent > params.max_rent):
                continue

            data_rows.append({
                "propertyId": pid,
                "title": title,
                "type": display_type,
                "target": row["rental_for"],
                "addedBy": row["created_by__name"],
                "areaSqft": detail.get("builtup_area_sqft"),
                "rooms": rooms,
                "features": features,
                "rent": rent,
                "status": "Active" if detail.get("current_status") == "Occupied" else "Inactive",
            })

        return data_rows

    @Common().exception_handler
    def rental_report_summary_extract(self, params: RentalReportRequest):
        data_rows = self._build_rental_report_rows(params)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_rental_report_summary,
                data={"totalProperties": len(data_rows)}
            )
        )

    @Common().exception_handler
    def rental_report_list_extract(self, params: RentalReportRequest):
        data_rows = self._build_rental_report_rows(params)

        pages = Paginator(data_rows, per_page=params.limit)
        if pages.num_pages and pages.num_pages < params.page_num:
            raise ValueError("Page limit exceed!")
        page_data = list(pages.page(params.page_num)) if pages.num_pages else []

        data = Utils.add_page_parameter(
            final_data=page_data,
            page_num=params.page_num,
            total_page=pages.num_pages,
            present_url=params.present_url,
            next_page_required=True if pages.num_pages != params.page_num else False,
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_rental_report_list, data=data)
        )

    @Common().exception_handler
    def assign_extract(self, params: PropertyAssignmentCreateRequest):
        from pms_apps.lead.models.lead import Lead
        
        # Validate property detail exists
        property_detail = PropertyDetail.objects.filter(property_id=params.property_id).first()
        if not property_detail:
            # Debug: Check if Property exists but PropertyDetail doesn't
            property_exists = Property.objects.filter(property_id=params.property_id).exists()
            if property_exists:
                raise ValueError(f"Property {params.property_id} exists but no PropertyDetail found. Please create property details first.")
            else:
                raise ValueError(f"Invalid Property ID: {params.property_id}. Property does not exist.")
        
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
            property_detail.current_tenant = params.tenant_id
            property_detail.current_status = "Booked"
            property_detail.save()
        
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_assign,
                data={"property_assignment_id": assignment_id}
            )
        )

    @Common().exception_handler
    def update_assignment_extract(self, params: PropertyAssignmentUpdateRequest):
        assignment_id = PropertyAssignment.update(
            property_assignment_id=params.property_assignment_id,
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
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_update,
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
                "tenantId": assignment.tenant_id if assignment.tenant else None,
                "firstName": assignment.tenant.first_name if assignment.tenant else None,
                "lastName": assignment.tenant.last_name if assignment.tenant else None,
                "phoneNumber": assignment.tenant.lead_id.phone_number if assignment.tenant and assignment.tenant.lead_id else None,
                "email": assignment.tenant.lead_id.email if assignment.tenant and assignment.tenant.lead_id else None,
            } if assignment.tenant else None,
            "assignedBy": {
                "userId": assignment.assigned_by.user_id if assignment.assigned_by else None,
                "phoneNumber": assignment.assigned_by.phone_number if assignment.assigned_by else None,
                "name": assignment.assigned_by.get_full_name() if assignment.assigned_by else None,
                "email": assignment.assigned_by.email if assignment.assigned_by else None,
            } if assignment.assigned_by else None,
            "assignmentStatus": assignment.assignment_status,
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
            'property', 'tenant', 'tenant__lead_id', 'assigned_by', 'agreement_prepared_by'
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
        paginator = Paginator(query, per_page=params.limit)
        
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
                    "tenantId": assignment.tenant_id if assignment.tenant else None,
                    "firstName": assignment.tenant.first_name if assignment.tenant else None,
                    "lastName": assignment.tenant.last_name if assignment.tenant else None,
                    "phoneNumber": assignment.tenant.lead_id.phone_number if assignment.tenant and assignment.tenant.lead_id else None,
                    "email": assignment.tenant.lead_id.email if assignment.tenant and assignment.tenant.lead_id else None,
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

    @Common().exception_handler
    def assignment_count_extract(self, params: GetAll):
        from django.db.models import Count, Q

        # Same "belongs to this user" scope as /property/count/ (created_by, assigned_to,
        # or landlord), not just assigned_to_id, so the two endpoints agree on the total.
        user_scope = (
            Q(created_by__user_id=params.user_id) |
            Q(assigned_to__user_id=params.user_id) |
            Q(propertydetail__landlord__lead_id__user_id=params.user_id)
        )

        # Total properties belonging to this user
        total_properties = Property.objects.filter(
            user_scope,
            is_active=True
        ).distinct().count()

        # Properties with a currently active tenancy (ended assignments keep their tenant FK, so
        # status must be checked too, not just tenant__isnull)
        from pms_apps.property.models.property_assignment import PropertyAssignment
        assigned_properties = Property.objects.filter(
            user_scope,
            is_active=True,
            assignments__tenant__isnull=False,
            assignments__assignment_status__in=["Active", "Approved"]
        ).distinct().count()
        
        # Unassigned properties
        unassigned_properties = total_properties - assigned_properties
        
        data = {
            'total_properties': total_properties,
            'assigned_properties': assigned_properties,
            'unassigned_properties': unassigned_properties
        }
        
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_assignment_count, data=data)
        )
