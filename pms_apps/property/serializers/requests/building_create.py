from rest_framework import serializers

from pms_apps.property.dataclasses.requests.building_create import BuildingCreateRequest


class BuildingCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    property_type = serializers.ChoiceField(
        choices=["Flat", "Commercial", "Villa", "Warehouse"],
        help_text="Locks which unit rental_type may be created under this building."
    )
    block = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    total_floors = serializers.IntegerField(required=False, allow_null=True)
    year_of_construction = serializers.IntegerField(required=False, allow_null=True)

    facilities = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True,
        help_text="Building-level common amenities, e.g. Parking, Lift, CCTV"
    )
    rental_purpose = serializers.ChoiceField(
        choices=["Residential", "Commercial"], required=False, allow_null=True
    )
    allowed_tenant_types = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True,
        help_text="e.g. Bachelor, Family, Company Staff, Labour"
    )

    # Flat-specific structured amenities
    parking = serializers.BooleanField(required=False, allow_null=True, default=False)
    lift = serializers.BooleanField(required=False, allow_null=True, default=False)
    security = serializers.BooleanField(required=False, allow_null=True, default=False)
    gas_pipeline = serializers.BooleanField(required=False, allow_null=True, default=False)
    water_supply = serializers.BooleanField(required=False, allow_null=True, default=False)
    intercom = serializers.BooleanField(required=False, allow_null=True, default=False)
    fire_safety = serializers.BooleanField(required=False, allow_null=True, default=False)

    # Villa-specific (required when property_type == "Villa")
    project_name = serializers.CharField(max_length=150, required=False, allow_null=True, allow_blank=True)
    private_garden = serializers.BooleanField(required=False, allow_null=True, default=False)
    private_parking = serializers.ChoiceField(
        choices=["Open", "Covered", "Both"], required=False, allow_null=True
    )
    swimming_pool = serializers.ChoiceField(
        choices=["No", "Private", "Common"], required=False, allow_null=True
    )
    terrace_access = serializers.BooleanField(required=False, allow_null=True, default=False)
    boundary_wall = serializers.BooleanField(required=False, allow_null=True, default=False)
    driveway = serializers.BooleanField(required=False, allow_null=True, default=False)
    water_supply_24x7 = serializers.BooleanField(required=False, allow_null=True, default=False)
    security_guard = serializers.BooleanField(required=False, allow_null=True, default=False)
    clubhouse_access = serializers.BooleanField(required=False, allow_null=True, default=False)
    gym = serializers.BooleanField(required=False, allow_null=True, default=False)
    childrens_play_area = serializers.BooleanField(required=False, allow_null=True, default=False)
    internal_roads = serializers.BooleanField(required=False, allow_null=True, default=False)
    street_lights = serializers.BooleanField(required=False, allow_null=True, default=False)
    gated_community = serializers.BooleanField(required=False, allow_null=True, default=False)

    # Shared between Flat and Villa
    power_backup = serializers.BooleanField(required=False, allow_null=True, default=False)

    # Commercial-specific (commercial_category required when property_type == "Commercial")
    commercial_category = serializers.ChoiceField(
        choices=["Shop", "Office", "Showroom", "Godown", "Industrial Unit"],
        required=False, allow_null=True
    )
    lift_type = serializers.ChoiceField(
        choices=["Passenger", "Goods", "Both"], required=False, allow_null=True
    )
    fire_safety_compliant = serializers.BooleanField(required=False, allow_null=True, default=False)
    emergency_exit = serializers.BooleanField(required=False, allow_null=True, default=False)
    parking_availability = serializers.ChoiceField(
        choices=["Open", "Covered", "Both"], required=False, allow_null=True
    )
    cctv = serializers.BooleanField(required=False, allow_null=True, default=False)

    # Warehouse-specific (warehouse_category/ownership_type required when property_type == "Warehouse")
    warehouse_category = serializers.ChoiceField(
        choices=["Industrial Warehouse", "Logistics Warehouse", "Cold Storage", "Godown"],
        required=False, allow_null=True
    )
    industrial_estate_name = serializers.CharField(max_length=150, required=False, allow_null=True, allow_blank=True)
    ownership_type = serializers.ChoiceField(
        choices=["Owned", "Leased"], required=False, allow_null=True
    )
    has_transformer = serializers.BooleanField(required=False, allow_null=True, default=False)
    water_supply_source = serializers.ChoiceField(
        choices=["Borewell", "Municipal", "Tanker"], required=False, allow_null=True
    )
    has_drainage_system = serializers.BooleanField(required=False, allow_null=True, default=False)
    has_internet_fiber = serializers.BooleanField(required=False, allow_null=True, default=False)
    allowed_industry_types = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True,
        help_text="e.g. FMCG, Pharma, Ecommerce, Manufacturing, Logistics"
    )

    # Shared between Commercial and Warehouse
    power_load_kw = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)
    has_dg_backup = serializers.BooleanField(required=False, allow_null=True, default=False)

    address_line_1 = serializers.CharField()
    address_line_2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    area_zone = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()
    pincode = serializers.CharField(max_length=10)
    google_map_location = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    internal_notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate(self, data):
        property_type = data.get('property_type')
        if property_type == 'Villa' and not data.get('project_name'):
            raise serializers.ValidationError({
                'project_name': 'This field is required when property_type is Villa.'
            })
        if property_type == 'Commercial' and not data.get('commercial_category'):
            raise serializers.ValidationError({
                'commercial_category': 'This field is required when property_type is Commercial.'
            })
        if property_type == 'Warehouse':
            missing = [f for f in ('warehouse_category', 'ownership_type') if not data.get(f)]
            if missing:
                raise serializers.ValidationError({
                    field: 'This field is required when property_type is Warehouse.' for field in missing
                })
        return data

    def create(self, validated_data) -> BuildingCreateRequest:
        return BuildingCreateRequest(**validated_data)
