from rest_framework import serializers
from pms_apps.property.dataclasses.requests.update import (
    PropertyUpdateRequest,
    PropertyDetailUpdateData,
    CommercialPropertyUpdateData,
    FlatPropertyUpdateData,
    VillaPropertyUpdateData
)
from pms_apps.property.serializers.fields import Base64ImageField


class UserRequestSerilizer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False, allow_null=True)


class PropertyDetailUpdateSerializer(serializers.Serializer):
    """Serializer for updating common property detail fields"""
    building_name = serializers.CharField(required=False, allow_null=True)
    total_floors = serializers.IntegerField(required=False, allow_null=True)
    carpet_area_sqft = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    builtup_area_sqft = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    monthly_rent = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    security_deposit_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    electricity_charge_type = serializers.ChoiceField(
        choices=["Meter", "Fixed"], required=False, allow_null=True
    )
    water_charge_type = serializers.ChoiceField(
        choices=["Meter", "Fixed"], required=False, allow_null=True
    )

    late_fee_type = serializers.ChoiceField(
        choices=["Percentage", "Fixed"], required=False, allow_null=True
    )
    late_fee_value = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)

    current_status = serializers.ChoiceField(
        choices=["Vacant", "Booked", "Occupied", "Under Maintenance"], required=False, allow_null=True
    )

    landlord_id = serializers.IntegerField(required=False, allow_null=True)
    address_line_1 = serializers.CharField(required=False, allow_null=True)
    address_line_2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    area_zone = serializers.CharField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)
    state = serializers.CharField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_null=True)
    pincode = serializers.CharField(max_length=10, required=False, allow_null=True)

    google_map_location = serializers.CharField(required=False, allow_null=True)

    year_of_construction = serializers.IntegerField(required=False, allow_null=True)
    other_charges = serializers.JSONField(required=False, allow_null=True)
    available_from = serializers.DateField(required=False, allow_null=True)
    current_tenant_id = serializers.IntegerField(required=False, allow_null=True)
    internal_notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class CommercialPropertyUpdateSerializer(serializers.Serializer):
    """Serializer for updating Commercial property specific fields"""
    commercial_category = serializers.ChoiceField(
        choices=["Shop", "Office", "Showroom", "Godown", "Industrial Unit"], required=False, allow_null=True
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
    has_dg_backup = serializers.BooleanField(required=False, allow_null=True)
    lift_type = serializers.ChoiceField(
        choices=["Passenger", "Goods", "Both"], required=False, allow_null=True
    )
    fire_safety_compliant = serializers.BooleanField(required=False, allow_null=True)
    emergency_exit = serializers.BooleanField(required=False, allow_null=True)
    parking_availability = serializers.ChoiceField(
        choices=["Open", "Covered", "Both"], required=False, allow_null=True
    )
    commercial_maintenance_charge_type = serializers.ChoiceField(
        choices=["Monthly", "Per SqFt"], required=False, allow_null=True
    )
    maintenance_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    gst_applicable = serializers.BooleanField(required=False, allow_null=True)
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


class FlatPropertyUpdateSerializer(serializers.Serializer):
    """Serializer for updating Flat property specific fields"""
    flat_number = serializers.CharField(max_length=50, required=False, allow_null=True)
    floor_number = serializers.IntegerField(required=False, allow_null=True)
    building_block = serializers.CharField(
        max_length=50, required=False, allow_null=True, allow_blank=True
    )
    flat_configuration = serializers.ChoiceField(
        choices=["Studio", "1BHK", "2BHK", "3BHK", "4BHK"], required=False, allow_null=True
    )
    no_of_bathrooms = serializers.IntegerField(required=False, allow_null=True)
    kitchen_type = serializers.ChoiceField(
        choices=["Open", "Closed"], required=False, allow_null=True
    )
    facing = serializers.ChoiceField(
        choices=["East", "West", "North", "South"], required=False, allow_null=True
    )
    balcony = serializers.BooleanField(required=False, allow_null=True)
    parking = serializers.BooleanField(required=False, allow_null=True)
    lift = serializers.BooleanField(required=False, allow_null=True)
    security = serializers.BooleanField(required=False, allow_null=True)
    gas_pipeline = serializers.BooleanField(required=False, allow_null=True)
    water_supply = serializers.BooleanField(required=False, allow_null=True)
    intercom = serializers.BooleanField(required=False, allow_null=True)
    fire_safety = serializers.BooleanField(required=False, allow_null=True)
    power_backup = serializers.BooleanField(required=False, allow_null=True)
    cctv = serializers.BooleanField(required=False, allow_null=True)
    allowed_tenant_types = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )
    store_room = serializers.BooleanField(required=False, allow_null=True)
    maintenance_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )


class VillaPropertyUpdateSerializer(serializers.Serializer):
    """Serializer for updating Villa property specific fields"""
    villa_name = serializers.CharField(max_length=150, required=False, allow_null=True)
    villa_type = serializers.ChoiceField(
        choices=["Independent", "Duplex", "Triplex"], required=False, allow_null=True
    )
    villa_configuration = serializers.ChoiceField(
        choices=["2BHK", "3BHK", "4BHK", "5BHK"], required=False, allow_null=True
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
    servant_room = serializers.BooleanField(required=False, allow_null=True)
    balcony_or_sitout = serializers.BooleanField(required=False, allow_null=True)
    private_garden = serializers.BooleanField(required=False, allow_null=True)
    terrace_access = serializers.BooleanField(required=False, allow_null=True)
    boundary_wall = serializers.BooleanField(required=False, allow_null=True)
    driveway = serializers.BooleanField(required=False, allow_null=True)
    private_parking = serializers.ChoiceField(
        choices=["Open", "Covered", "Both"], required=False, allow_null=True
    )
    villa_maintenance_charge_type = serializers.ChoiceField(
        choices=["Monthly", "Yearly"], required=False, allow_null=True
    )
    gardening_charges = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    water_supply_24x7 = serializers.BooleanField(required=False, allow_null=True)
    security_guard = serializers.BooleanField(required=False, allow_null=True)
    clubhouse_access = serializers.BooleanField(required=False, allow_null=True)
    gym = serializers.BooleanField(required=False, allow_null=True)
    childrens_play_area = serializers.BooleanField(required=False, allow_null=True)
    internal_roads = serializers.BooleanField(required=False, allow_null=True)
    street_lights = serializers.BooleanField(required=False, allow_null=True)
    gated_community = serializers.BooleanField(required=False, allow_null=True)
    bachelor_allowed = serializers.BooleanField(required=False, allow_null=True)
    pets_allowed = serializers.BooleanField(required=False, allow_null=True)
    power_backup = serializers.BooleanField(required=False, allow_null=True)
    cctv = serializers.BooleanField(required=False, allow_null=True)
    allowed_tenant_types = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )
    store_room = serializers.BooleanField(required=False, allow_null=True)
    maintenance_charge_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )


class PropertyUpdateSerializer(serializers.Serializer):
    property_id = serializers.IntegerField()
    block = serializers.CharField(max_length=50, required=False, allow_null=True)
    building_details = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    floor = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    flat_number = serializers.IntegerField(required=False, allow_null=True)
    dimension_length_ft = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    dimension_breadth_ft = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    dimension_area_sqft = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    rental_type = serializers.ChoiceField(choices=["Flat", "Commercial", "Villa"], required=False, allow_null=True)
    rental_for = serializers.ChoiceField(choices=["Bachelor", "Family", "Labour"], required=False, allow_null=True)
    advance_amount_rent = serializers.IntegerField(required=False, allow_null=True)
    expected_rent = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    agreement_id = serializers.IntegerField(required=False, allow_null=True)
    photos = serializers.ListField(child=Base64ImageField(), required=False, allow_null=True)
    videos = serializers.ListField(child=serializers.URLField(), required=False, allow_null=True)
    assigned_to = UserRequestSerilizer(required=False, allow_null=True)

    property_details = PropertyDetailUpdateSerializer(required=False, allow_null=True)
    commercial_data = CommercialPropertyUpdateSerializer(required=False, allow_null=True)
    flat_data = FlatPropertyUpdateSerializer(required=False, allow_null=True)
    villa_data = VillaPropertyUpdateSerializer(required=False, allow_null=True)

    def create(self, validated_data) -> PropertyUpdateRequest:
        property_details_dict = validated_data.pop('property_details', None)
        commercial_data_dict = validated_data.pop('commercial_data', None)
        flat_data_dict = validated_data.pop('flat_data', None)
        villa_data_dict = validated_data.pop('villa_data', None)
        assigned_user_data = validated_data.pop('assigned_to', None)
        
        property_details = None
        if property_details_dict:
            property_details = PropertyDetailUpdateData(**property_details_dict)
        
        commercial_data = None
        if commercial_data_dict:
            commercial_data = CommercialPropertyUpdateData(**commercial_data_dict)
            
        flat_data = None
        if flat_data_dict:
            flat_data = FlatPropertyUpdateData(**flat_data_dict)
            
        villa_data = None
        if villa_data_dict:
            villa_data = VillaPropertyUpdateData(**villa_data_dict)

        assigned_to_user_id = assigned_user_data.get('user_id') if assigned_user_data else None
        
        return PropertyUpdateRequest(
            **validated_data,
            property_details=property_details,
            commercial_data=commercial_data,
            flat_data=flat_data,
            villa_data=villa_data,
            assigned_to=assigned_to_user_id
        )