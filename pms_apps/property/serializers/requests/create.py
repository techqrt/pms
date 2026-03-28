from rest_framework import serializers
from pms_apps.property.dataclasses.requests.create import PropertyCreateRequest as PropertyCreateRequest
from pms_apps.authentication.serializers.request.create import PropertyUserSerializer
from pms_apps.property.serializers.fields import Base64ImageField


class UserRequestSerilizer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False, allow_null=True)


class PropertyCommonDataSerializer(serializers.Serializer):
    building_name = serializers.CharField()
    total_floors = serializers.IntegerField()
    carpet_area_sqft = serializers.DecimalField(max_digits=10, decimal_places=2)
    builtup_area_sqft = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_rent = serializers.DecimalField(max_digits=12, decimal_places=2)
    security_deposit_amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    electricity_charge_type = serializers.ChoiceField(
        choices=["Meter", "Fixed"]
    )
    water_charge_type = serializers.ChoiceField(
        choices=["Meter", "Fixed"]
    )

    late_fee_type = serializers.ChoiceField(
        choices=["Percentage", "Fixed"]
    )
    late_fee_value = serializers.DecimalField(max_digits=8, decimal_places=2)

    current_status = serializers.ChoiceField(
        choices=["Vacant", "Booked", "Occupied", "Under Maintenance"]
    )

    landlord_id = serializers.IntegerField()
    created_by_id = serializers.IntegerField()

    address_line_1 = serializers.CharField()
    address_line_2 = serializers.CharField()

    area_zone = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()
    pincode = serializers.CharField(max_length=10)

    google_map_location = serializers.CharField()

    year_of_construction = serializers.IntegerField()
    other_charges = serializers.JSONField(required=False, allow_null=True, default=dict)
    available_from = serializers.DateField(required=False, allow_null=True)
    current_tenant_id = serializers.IntegerField(required=False, allow_null=True)
    internal_notes = serializers.CharField()


class CommercialPropertySerializer(serializers.Serializer):
    commercial_category = serializers.ChoiceField(
        choices=["Shop", "Office", "Showroom", "Godown", "Industrial Unit"]
    )
    floor_number = serializers.IntegerField(required=False, allow_null=True)
    frontage_width_ft = serializers.DecimalField(
        max_digits=6, decimal_places=2, required=False, allow_null=True
    )
    ceiling_height_ft = serializers.DecimalField(
        max_digits=6, decimal_places=2, required=False, allow_null=True
    )
    no_of_cabins = serializers.IntegerField(required=False, allow_null=True)
    no_of_washrooms = serializers.IntegerField(required=False, allow_null=True)
    loading_area = serializers.ChoiceField(
        choices=["Warehouse", "Godown"], required=False, allow_null=True
    )
    power_load_kw = serializers.DecimalField(
        max_digits=6, decimal_places=2, required=False, allow_null=True
    )
    has_dg_backup = serializers.BooleanField(required=False, allow_null=True, default=False)
    lift_type = serializers.ChoiceField(
        choices=["Passenger", "Goods", "Both"], required=False, allow_null=True
    )
    fire_safety_compliant = serializers.BooleanField(required=False, allow_null=True, default=False)
    emergency_exit = serializers.BooleanField(required=False, allow_null=True, default=False)
    parking_availability = serializers.ChoiceField(
        choices=["Open", "Covered", "Both"], required=False, allow_null=True
    )
    commercial_maintenance_charge_type = serializers.ChoiceField(
        choices=["Monthly", "Per SqFt"], required=False, allow_null=True
    )
    maintenance_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    electricity_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    water_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    gst_applicable = serializers.BooleanField(required=False, allow_null=True, default=False)
    gst_percentage = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False, allow_null=True
    )
    security_deposit_months = serializers.IntegerField(required=False, allow_null=True)
    lease_type = serializers.ChoiceField(
        choices=["Company", "Individual"], required=False, allow_null=True
    )
    lease_tenure_years = serializers.IntegerField(required=False, allow_null=True)
    lock_in_period_months = serializers.IntegerField(required=False, allow_null=True)
    allowed_business = serializers.CharField(required=False, allow_null=True)
    prohibited_business = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class FlatPropertySerializer(serializers.Serializer):
    flat_number = serializers.CharField(max_length=50)
    floor_number = serializers.IntegerField(required=False, allow_null=True)
    building_block = serializers.CharField(
        max_length=50, required=False, allow_null=True, allow_blank=True
    )
    flat_configuration = serializers.ChoiceField(
        choices=["Studio", "1BHK", "2BHK", "3BHK", "4BHK"]
    )
    no_of_bathrooms = serializers.IntegerField(required=False, allow_null=True)
    kitchen_type = serializers.ChoiceField(
        choices=["Open", "Closed"], required=False, allow_null=True
    )
    facing = serializers.ChoiceField(
        choices=["East", "West", "North", "South"], required=False, allow_null=True
    )
    balcony = serializers.BooleanField(required=False, allow_null=True, default=False)
    parking = serializers.BooleanField(required=False, allow_null=True, default=False)
    lift = serializers.BooleanField(required=False, allow_null=True, default=False)
    security = serializers.BooleanField(required=False, allow_null=True, default=False)
    gas_pipeline = serializers.BooleanField(required=False, allow_null=True, default=False)
    water_supply = serializers.BooleanField(required=False, allow_null=True, default=False)
    intercom = serializers.BooleanField(required=False, allow_null=True, default=False)
    fire_safety = serializers.BooleanField(required=False, allow_null=True, default=False)
    power_backup = serializers.BooleanField(required=False, allow_null=True, default=False)
    cctv = serializers.BooleanField(required=False, allow_null=True, default=False)
    allowed_tenant_types = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )
    store_room = serializers.BooleanField(required=False, allow_null=True, default=False)
    maintenance_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    electricity_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    water_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )


class VillaPropertySerializer(serializers.Serializer):
    villa_name = serializers.CharField(max_length=150)
    villa_type = serializers.ChoiceField(
        choices=["Independent", "Duplex", "Triplex"]
    )
    villa_configuration = serializers.ChoiceField(
        choices=["2BHK", "3BHK", "4BHK", "5BHK"]
    )
    project_name = serializers.CharField(
        max_length=150, required=False, allow_null=True, allow_blank=True
    )
    plot_area_sqft = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    number_of_bedrooms = serializers.IntegerField(required=False, allow_null=True)
    number_of_bathrooms = serializers.IntegerField(required=False, allow_null=True)
    living_rooms_count = serializers.IntegerField(required=False, allow_null=True)
    servant_room = serializers.BooleanField(required=False, allow_null=True, default=False)
    balcony_or_sitout = serializers.BooleanField(required=False, allow_null=True, default=False)
    private_garden = serializers.BooleanField(required=False, allow_null=True, default=False)
    terrace_access = serializers.BooleanField(required=False, allow_null=True, default=False)
    boundary_wall = serializers.BooleanField(required=False, allow_null=True, default=False)
    driveway = serializers.BooleanField(required=False, allow_null=True, default=False)
    private_parking = serializers.ChoiceField(
        choices=["Open", "Covered", "Both"], required=False, allow_null=True
    )
    villa_maintenance_charge_type = serializers.ChoiceField(
        choices=["Monthly", "Yearly"], required=False, allow_null=True
    )
    gardening_charges = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    water_supply_24x7 = serializers.BooleanField(required=False, allow_null=True, default=False)
    security_guard = serializers.BooleanField(required=False, allow_null=True, default=False)
    clubhouse_access = serializers.BooleanField(required=False, allow_null=True, default=False)
    gym = serializers.BooleanField(required=False, allow_null=True, default=False)
    childrens_play_area = serializers.BooleanField(required=False, allow_null=True, default=False)
    internal_roads = serializers.BooleanField(required=False, allow_null=True, default=False)
    street_lights = serializers.BooleanField(required=False, allow_null=True, default=False)
    gated_community = serializers.BooleanField(required=False, allow_null=True, default=False)
    bachelor_allowed = serializers.BooleanField(required=False, allow_null=True, default=False)
    pets_allowed = serializers.BooleanField(required=False, allow_null=True, default=False)
    power_backup = serializers.BooleanField(required=False, allow_null=True, default=False)
    cctv = serializers.BooleanField(required=False, allow_null=True, default=False)
    allowed_tenant_types = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )
    store_room = serializers.BooleanField(required=False, allow_null=True, default=False)
    maintenance_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    electricity_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    water_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )


class PropertyCreateSerializer(serializers.Serializer):
    block = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    building_details = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    floor = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    flat_number = serializers.IntegerField(required=False, allow_null=True)
    dimension_length_ft = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    dimension_breadth_ft = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    dimension_area_sqft = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )
    rental_type = serializers.ChoiceField(choices=["Flat", "Commercial", "Villa"])
    rental_for = serializers.ChoiceField(
        choices=["Bachelor", "Family", "Labour"], required=False, default="Family"
    )
    advance_amount_rent = serializers.IntegerField(required=False, allow_null=True)
    expected_rent = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )
    agreement_id = serializers.IntegerField(required=False, allow_null=True)
    photos = serializers.ListField(
        child=Base64ImageField(), required=False, allow_null=True
    )
    videos = serializers.ListField(
        child=serializers.URLField(), required=False, allow_null=True
    )
    assigned_to = UserRequestSerilizer(required=False, allow_null=True)

    property_details = PropertyCommonDataSerializer()

    commercial_data = CommercialPropertySerializer(required=False, allow_null=True)
    flat_data = FlatPropertySerializer(required=False, allow_null=True)
    villa_data = VillaPropertySerializer(required=False, allow_null=True)

    def validate(self, data):
        """Validate that the correct property type data is provided based on rental_type"""
        rental_type = data.get('rental_type')
        
        if rental_type == 'Commercial':
            if not data.get('commercial_data'):
                raise serializers.ValidationError({
                    'commercial_data': 'Commercial property data is required for Commercial rental type.'
                })
            if data.get('flat_data') or data.get('villa_data'):
                raise serializers.ValidationError({
                    'property_type_data': 'Only commercial_data should be provided for Commercial rental type.'
                })
        
        elif rental_type == 'Flat':
            if not data.get('flat_data'):
                raise serializers.ValidationError({
                    'flat_data': 'Flat property data is required for Flat rental type.'
                })
            if data.get('commercial_data') or data.get('villa_data'):
                raise serializers.ValidationError({
                    'property_type_data': 'Only flat_data should be provided for Flat rental type.'
                })
        
        elif rental_type == 'Villa':
            if not data.get('villa_data'):
                raise serializers.ValidationError({
                    'villa_data': 'Villa property data is required for Villa rental type.'
                })
            if data.get('commercial_data') or data.get('flat_data'):
                raise serializers.ValidationError({
                    'property_type_data': 'Only villa_data should be provided for Villa rental type.'
                })
        
        return data

    def create(self, validated_data) -> PropertyCreateRequest:
        from pms_apps.property.dataclasses.requests.create import (
            PropertyCommonData,
            CommercialPropertyData,
            FlatPropertyData,
            VillaPropertyData
        )
        
        commercial_data_dict = validated_data.pop('commercial_data', None)
        flat_data_dict = validated_data.pop('flat_data', None)
        villa_data_dict = validated_data.pop('villa_data', None)
        property_details_dict = validated_data.pop('property_details')
        assigned_to = validated_data.pop('assigned_to', None)
        photos = validated_data.pop('photos', [])
        videos = validated_data.pop('videos', [])
        
        property_details = PropertyCommonData(**property_details_dict)
        
        commercial_data = None
        if commercial_data_dict:
            commercial_data = CommercialPropertyData(**commercial_data_dict)
        
        flat_data = None
        if flat_data_dict:
            flat_data = FlatPropertyData(**flat_data_dict)
        
        villa_data = None
        if villa_data_dict:
            villa_data = VillaPropertyData(**villa_data_dict)
        
        return PropertyCreateRequest(
            **validated_data,
            property_details=property_details,
            commercial_data=commercial_data,
            flat_data=flat_data,
            villa_data=villa_data,
            assigned_to=assigned_to,
            photos=photos or [],
            videos=videos or []
        )