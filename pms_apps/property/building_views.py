from django.db import transaction
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response

from pms.constants import Constants
from pms_apps.common.common import Common
from pms_apps.common.dataclasses.get_all import GetAll
from pms_apps.common.utils import Utils

from pms_apps.property.dataclasses.requests.building_create import BuildingCreateRequest
from pms_apps.property.dataclasses.requests.building_update import BuildingUpdateRequest
from pms_apps.property.dataclasses.requests.building_get import BuildingGetRequest
from pms_apps.property.dataclasses.requests.building_delete import BuildingDeleteRequest

from pms_apps.property.models.building import Building
from pms_apps.property.serializers.response.building_get_all import BuildingResponseGetAllSerializer


def _building_to_camel_case(row: dict) -> dict:
    return {
        'buildingId': row.get('building_id'),
        'name': row.get('name'),
        'propertyType': row.get('property_type'),
        'block': row.get('block'),
        'totalFloors': row.get('total_floors'),
        'yearOfConstruction': row.get('year_of_construction'),
        'facilities': row.get('facilities') or [],
        'rentalPurpose': row.get('rental_purpose'),
        'allowedTenantTypes': row.get('allowed_tenant_types') or [],
        'parking': row.get('parking'),
        'lift': row.get('lift'),
        'security': row.get('security'),
        'gasPipeline': row.get('gas_pipeline'),
        'waterSupply': row.get('water_supply'),
        'intercom': row.get('intercom'),
        'fireSafety': row.get('fire_safety'),
        'projectName': row.get('project_name'),
        'privateGarden': row.get('private_garden'),
        'privateParking': row.get('private_parking'),
        'swimmingPool': row.get('swimming_pool'),
        'terraceAccess': row.get('terrace_access'),
        'boundaryWall': row.get('boundary_wall'),
        'driveway': row.get('driveway'),
        'waterSupply24x7': row.get('water_supply_24x7'),
        'securityGuard': row.get('security_guard'),
        'clubhouseAccess': row.get('clubhouse_access'),
        'gym': row.get('gym'),
        'childrensPlayArea': row.get('childrens_play_area'),
        'internalRoads': row.get('internal_roads'),
        'streetLights': row.get('street_lights'),
        'gatedCommunity': row.get('gated_community'),
        'powerBackup': row.get('power_backup'),
        'commercialCategory': row.get('commercial_category'),
        'liftType': row.get('lift_type'),
        'fireSafetyCompliant': row.get('fire_safety_compliant'),
        'emergencyExit': row.get('emergency_exit'),
        'parkingAvailability': row.get('parking_availability'),
        'cctv': row.get('cctv'),
        'warehouseCategory': row.get('warehouse_category'),
        'industrialEstateName': row.get('industrial_estate_name'),
        'ownershipType': row.get('ownership_type'),
        'hasTransformer': row.get('has_transformer'),
        'waterSupplySource': row.get('water_supply_source'),
        'hasDrainageSystem': row.get('has_drainage_system'),
        'hasInternetFiber': row.get('has_internet_fiber'),
        'allowedIndustryTypes': row.get('allowed_industry_types') or [],
        'powerLoadKw': row.get('power_load_kw'),
        'hasDgBackup': row.get('has_dg_backup'),
        'addressLine1': row.get('address_line_1'),
        'addressLine2': row.get('address_line_2'),
        'areaZone': row.get('area_zone'),
        'city': row.get('city'),
        'state': row.get('state'),
        'country': row.get('country'),
        'pincode': row.get('pincode'),
        'googleMapLocation': row.get('google_map_location'),
        'internalNotes': row.get('internal_notes'),
        'createdBy': {
            'userId': row.get('created_by__user_id'),
            'name': row.get('created_by__name'),
        } if row.get('created_by__user_id') else None,
        'createdAt': row.get('created_at'),
        'updatedAt': row.get('updated_at'),
        'isActive': row.get('is_active'),
    }


# noinspection PyMethodParameters
class BuildingView:
    def __init__(self) -> None:
        super().__init__()
        self.data_create = "Building added successfully"
        self.data_update = "Building updated successfully"
        self.data_delete = "Building deleted successfully"
        self.data_get = "Building fetched successfully"
        self.data_no_match = "No matching building found"

    @Common().exception_handler
    def create_extract(self, params: BuildingCreateRequest):
        with transaction.atomic():
            building = Building()
            building_id = building.create(
                name=params.name,
                property_type=params.property_type,
                block=params.block,
                total_floors=params.total_floors,
                year_of_construction=params.year_of_construction,
                facilities=params.facilities,
                rental_purpose=params.rental_purpose,
                allowed_tenant_types=params.allowed_tenant_types,
                parking=params.parking,
                lift=params.lift,
                security=params.security,
                gas_pipeline=params.gas_pipeline,
                water_supply=params.water_supply,
                intercom=params.intercom,
                fire_safety=params.fire_safety,
                project_name=params.project_name,
                private_garden=params.private_garden,
                private_parking=params.private_parking,
                swimming_pool=params.swimming_pool,
                terrace_access=params.terrace_access,
                boundary_wall=params.boundary_wall,
                driveway=params.driveway,
                water_supply_24x7=params.water_supply_24x7,
                security_guard=params.security_guard,
                clubhouse_access=params.clubhouse_access,
                gym=params.gym,
                childrens_play_area=params.childrens_play_area,
                internal_roads=params.internal_roads,
                street_lights=params.street_lights,
                gated_community=params.gated_community,
                power_backup=params.power_backup,
                commercial_category=params.commercial_category,
                lift_type=params.lift_type,
                fire_safety_compliant=params.fire_safety_compliant,
                emergency_exit=params.emergency_exit,
                parking_availability=params.parking_availability,
                cctv=params.cctv,
                warehouse_category=params.warehouse_category,
                industrial_estate_name=params.industrial_estate_name,
                ownership_type=params.ownership_type,
                has_transformer=params.has_transformer,
                water_supply_source=params.water_supply_source,
                has_drainage_system=params.has_drainage_system,
                has_internet_fiber=params.has_internet_fiber,
                allowed_industry_types=params.allowed_industry_types,
                power_load_kw=params.power_load_kw,
                has_dg_backup=params.has_dg_backup,
                address_line_1=params.address_line_1,
                address_line_2=params.address_line_2,
                area_zone=params.area_zone,
                city=params.city,
                state=params.state,
                country=params.country,
                pincode=params.pincode,
                google_map_location=params.google_map_location,
                internal_notes=params.internal_notes,
                created_by=params.user_id,
            )

        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(message=self.data_create, data={'building_id': building_id})
        )

    @Common().exception_handler
    def update_extract(self, params: BuildingUpdateRequest):
        building_obj = Building.get(building_id=params.building_id)
        if not building_obj:
            raise ValueError(self.data_no_match)

        if params.property_type:
            from pms_apps.property.models.property import Property
            conflicting = Property.objects.filter(
                building_id=params.building_id, is_active=True
            ).exclude(rental_type=params.property_type).exists()
            if conflicting:
                raise ValueError(
                    f"Cannot set property_type to '{params.property_type}': this building "
                    f"already has units of a different type. Reassign or remove them first."
                )

        with transaction.atomic():
            Building.update(
                building_id=params.building_id,
                name=params.name,
                property_type=params.property_type,
                block=params.block,
                total_floors=params.total_floors,
                year_of_construction=params.year_of_construction,
                facilities=params.facilities,
                rental_purpose=params.rental_purpose,
                allowed_tenant_types=params.allowed_tenant_types,
                parking=params.parking,
                lift=params.lift,
                security=params.security,
                gas_pipeline=params.gas_pipeline,
                water_supply=params.water_supply,
                intercom=params.intercom,
                fire_safety=params.fire_safety,
                project_name=params.project_name,
                private_garden=params.private_garden,
                private_parking=params.private_parking,
                swimming_pool=params.swimming_pool,
                terrace_access=params.terrace_access,
                boundary_wall=params.boundary_wall,
                driveway=params.driveway,
                water_supply_24x7=params.water_supply_24x7,
                security_guard=params.security_guard,
                clubhouse_access=params.clubhouse_access,
                gym=params.gym,
                childrens_play_area=params.childrens_play_area,
                internal_roads=params.internal_roads,
                street_lights=params.street_lights,
                gated_community=params.gated_community,
                power_backup=params.power_backup,
                commercial_category=params.commercial_category,
                lift_type=params.lift_type,
                fire_safety_compliant=params.fire_safety_compliant,
                emergency_exit=params.emergency_exit,
                parking_availability=params.parking_availability,
                cctv=params.cctv,
                warehouse_category=params.warehouse_category,
                industrial_estate_name=params.industrial_estate_name,
                ownership_type=params.ownership_type,
                has_transformer=params.has_transformer,
                water_supply_source=params.water_supply_source,
                has_drainage_system=params.has_drainage_system,
                has_internet_fiber=params.has_internet_fiber,
                allowed_industry_types=params.allowed_industry_types,
                power_load_kw=params.power_load_kw,
                has_dg_backup=params.has_dg_backup,
                address_line_1=params.address_line_1,
                address_line_2=params.address_line_2,
                area_zone=params.area_zone,
                city=params.city,
                state=params.state,
                country=params.country,
                pincode=params.pincode,
                google_map_location=params.google_map_location,
                internal_notes=params.internal_notes,
            )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_update, data={'building_id': params.building_id})
        )

    @Common().exception_handler
    def get_extract(self, params: BuildingGetRequest):
        building_data = Building.get(building_id=params.building_id)
        if not building_data:
            raise ValueError(self.data_no_match)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=_building_to_camel_case(building_data))
        )

    @Common(response_handler=BuildingResponseGetAllSerializer).exception_handler
    def get_all_extract(self, params: GetAll):
        building_list = Building.get_all(search_key=params.search_key)

        pages = Paginator(building_list, per_page=params.limit)

        if pages.num_pages and pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)

        page_data = pages.page(params.page_num) if pages.num_pages else []
        serialized = [_building_to_camel_case(row) for row in page_data]

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=None,
                data={
                    'data': serialized,
                    'presentPage': params.page_num,
                    'totalPage': pages.num_pages,
                }
            )
        )

    @Common().exception_handler
    def delete_extract(self, params: BuildingDeleteRequest):
        building_obj = Building.get(building_id=params.building_id)
        if not building_obj:
            raise ValueError(self.data_no_match)

        from pms_apps.property.models.property import Property
        if Property.objects.filter(building_id=params.building_id, is_active=True).exists():
            raise ValueError(
                "Cannot delete a building that still has units. Reassign or remove its units first."
            )

        with transaction.atomic():
            Building.delete(building_id=params.building_id)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_delete)
        )
