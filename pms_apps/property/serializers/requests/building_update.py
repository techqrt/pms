from rest_framework import serializers

from pms_apps.property.dataclasses.requests.building_update import BuildingUpdateRequest
from pms_apps.property.serializers.fields import Base64ImageField


class BuildingUpdateSerializer(serializers.Serializer):
    building_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    property_type = serializers.ChoiceField(
        choices=["Flat", "Commercial", "Villa", "Warehouse"], required=False, allow_null=True
    )
    block = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    total_floors = serializers.IntegerField(required=False, allow_null=True)
    year_of_construction = serializers.IntegerField(required=False, allow_null=True)

    facilities = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )
    rental_purpose = serializers.ChoiceField(
        choices=["Residential", "Commercial"], required=False, allow_null=True
    )
    allowed_tenant_types = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )

    parking = serializers.BooleanField(required=False, allow_null=True)
    lift = serializers.BooleanField(required=False, allow_null=True)
    security = serializers.BooleanField(required=False, allow_null=True)
    gas_pipeline = serializers.BooleanField(required=False, allow_null=True)
    water_supply = serializers.BooleanField(required=False, allow_null=True)
    intercom = serializers.BooleanField(required=False, allow_null=True)
    fire_safety = serializers.BooleanField(required=False, allow_null=True)

    project_name = serializers.CharField(max_length=150, required=False, allow_null=True, allow_blank=True)
    private_garden = serializers.BooleanField(required=False, allow_null=True)
    private_parking = serializers.ChoiceField(
        choices=["Open", "Covered", "Both"], required=False, allow_null=True
    )
    swimming_pool = serializers.ChoiceField(
        choices=["No", "Private", "Common"], required=False, allow_null=True
    )
    terrace_access = serializers.BooleanField(required=False, allow_null=True)
    boundary_wall = serializers.BooleanField(required=False, allow_null=True)
    driveway = serializers.BooleanField(required=False, allow_null=True)
    water_supply_24x7 = serializers.BooleanField(required=False, allow_null=True)
    security_guard = serializers.BooleanField(required=False, allow_null=True)
    clubhouse_access = serializers.BooleanField(required=False, allow_null=True)
    gym = serializers.BooleanField(required=False, allow_null=True)
    childrens_play_area = serializers.BooleanField(required=False, allow_null=True)
    internal_roads = serializers.BooleanField(required=False, allow_null=True)
    street_lights = serializers.BooleanField(required=False, allow_null=True)
    gated_community = serializers.BooleanField(required=False, allow_null=True)
    power_backup = serializers.BooleanField(required=False, allow_null=True)

    commercial_category = serializers.ChoiceField(
        choices=["Shop", "Office", "Showroom", "Godown", "Industrial Unit"],
        required=False, allow_null=True
    )
    lift_type = serializers.ChoiceField(
        choices=["Passenger", "Goods", "Both"], required=False, allow_null=True
    )
    fire_safety_compliant = serializers.BooleanField(required=False, allow_null=True)
    emergency_exit = serializers.BooleanField(required=False, allow_null=True)
    parking_availability = serializers.ChoiceField(
        choices=["Open", "Covered", "Both"], required=False, allow_null=True
    )
    cctv = serializers.BooleanField(required=False, allow_null=True)

    warehouse_category = serializers.ChoiceField(
        choices=["Industrial Warehouse", "Logistics Warehouse", "Cold Storage", "Godown"],
        required=False, allow_null=True
    )
    industrial_estate_name = serializers.CharField(max_length=150, required=False, allow_null=True, allow_blank=True)
    ownership_type = serializers.ChoiceField(
        choices=["Owned", "Leased"], required=False, allow_null=True
    )
    has_transformer = serializers.BooleanField(required=False, allow_null=True)
    water_supply_source = serializers.ChoiceField(
        choices=["Borewell", "Municipal", "Tanker"], required=False, allow_null=True
    )
    has_drainage_system = serializers.BooleanField(required=False, allow_null=True)
    has_internet_fiber = serializers.BooleanField(required=False, allow_null=True)
    allowed_industry_types = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )

    power_load_kw = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)
    has_dg_backup = serializers.BooleanField(required=False, allow_null=True)

    address_line_1 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    address_line_2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    area_zone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    city = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    state = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    country = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    pincode = serializers.CharField(max_length=10, required=False, allow_null=True, allow_blank=True)
    google_map_location = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    internal_notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    photos = serializers.ListField(
        child=Base64ImageField(), required=False, allow_null=True
    )

    def create(self, validated_data) -> BuildingUpdateRequest:
        return BuildingUpdateRequest(**validated_data)
