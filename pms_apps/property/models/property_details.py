from django.db import models
import uuid

class PropertyDetail(models.Model):
    ELECTRICITY_CHARGE_TYPE_CHOICES = [
        ("Meter", "Meter"),
        ("Fixed", "Fixed"),
    ]

    WATER_CHARGE_TYPE_CHOICES = [
        ("Meter", "Meter"),
        ("Fixed", "Fixed"),
    ]

    LATE_FEE_TYPE_CHOICES = [
        ("Day wise", "Day wise"),
        ("Month wise", "Month wise"),
    ]

    STATUS_CHOICES = [
        ("Vacant", "Vacant"),
        ("Booked", "Booked"),
        ("Occupied", "Occupied"),
        ("Under Maintenance", "Under Maintenance"),
    ]

    property_detail_id = models.AutoField(primary_key=True)
    property = models.ForeignKey("property.Property", on_delete=models.CASCADE)
    property_code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    building_name = models.CharField(max_length=150)
    total_floors = models.PositiveIntegerField()
    year_of_construction = models.PositiveIntegerField()

    carpet_area_sqft = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    builtup_area_sqft = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    monthly_rent = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    security_deposit_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    electricity_charge_type = models.CharField(
        max_length=20,
        choices=ELECTRICITY_CHARGE_TYPE_CHOICES,
        null=True,
        blank=True
    )

    water_charge_type = models.CharField(
        max_length=20,
        choices=WATER_CHARGE_TYPE_CHOICES,
        null=True,
        blank=True
    )

    other_charges = models.JSONField(
        default=dict,
        blank=True
    )

    late_fee_type = models.CharField(
        max_length=20,
        choices=LATE_FEE_TYPE_CHOICES
    )

    late_fee_value = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    current_status = models.CharField(
    max_length=30,
    choices=STATUS_CHOICES
    )

    available_from = models.DateField(
        null=True,
        blank=True
    )

    landlord = models.ForeignKey(
        "lead.Lead",  
        on_delete=models.PROTECT,
        related_name="properties_as_landlord"
    )

    current_tenant = models.CharField(
        max_length=250,
        null=True,
        blank=True
    )

    address_line_1 = models.TextField()

    address_line_2 = models.TextField(
        blank=True
    )

    area_zone = models.CharField(
        max_length=100
    )

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    country = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    google_map_location = models.TextField()


    internal_notes = models.TextField(
        blank=True
    )
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.DO_NOTHING
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    status_change_log = models.JSONField(
        default=list,
        blank=True
    )

    #Commercial Specific
    COMMERCIAL_CATEGORY_CHOICES = [
        ("Shop", "Shop"),
        ("Office", "Office"),
        ("Showroom", "Showroom"),
        ("Godown", "Godown"),
        ("Industrial Unit", "Industrial Unit"),
    ]

    commercial_category = models.CharField(
        max_length=30,
        choices=COMMERCIAL_CATEGORY_CHOICES,
        null=True,blank=True
    )

    frontage_width_ft = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,blank=True
    )
    ceiling_height_ft = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,blank=True
    )

    no_of_cabins = models.PositiveIntegerField(null=True)
    no_of_washrooms = models.PositiveIntegerField(null=True)

    LOADING_AREA_CHOICES = [
    ("Warehouse", "Warehouse"),
    ("Godown", "Godown"),
    ]
    loading_area = models.CharField(
        max_length=12,
        choices=LOADING_AREA_CHOICES,
        null=True
    )
    power_load_kw = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True
    )
    has_dg_backup = models.BooleanField(default=False,null=True)

    LIFT_TYPE_CHOICES = [
        ("Passenger", "Passenger"),
        ("Goods", "Goods"),
        ("Both", "Both"),
    ]
    lift_type = models.CharField(
        max_length=20,
        choices=LIFT_TYPE_CHOICES,null=True
    )
    fire_safety_compliant = models.BooleanField(default=False,null=True)
    emergency_exit = models.BooleanField(default=False,null=True)

    PARKING_AVAILABILITY_CHOICES = [
        ("Open", "Open"),
        ("Covered", "Covered"),
        ("Both", "Both"),
    ]
    parking_availability = models.CharField(
        max_length=20,
        choices=PARKING_AVAILABILITY_CHOICES,
        null=True
    )

    COMMERCIAL_MAINTENANCE_TYPE_CHOICES = [
        ("Monthly", "Monthly"),
        ("Per SqFt", "Per SqFt"),
    ]

    commercial_maintenance_charge_type = models.CharField(
        max_length=20,
        choices=COMMERCIAL_MAINTENANCE_TYPE_CHOICES,
        null=True
    )

    gst_applicable = models.BooleanField(default=False,null=True)
    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    security_deposit_months = models.PositiveIntegerField(null=True)

    LEASE_TYPE_CHOICES = [
        ("Company", "Company"),
        ("Individual", "Individual"),
    ]
    lease_type = models.CharField(
        max_length=20,
        choices=LEASE_TYPE_CHOICES,null=True
    )
    lease_tenure_years = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    lock_in_period_months = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    allowed_business = models.TextField(null=True,)
    prohibited_business = models.TextField(null=True,blank=True)

    #flat
    building_block = models.CharField(
        max_length=50,
        blank=True,null=True
    )
    flat_number = models.CharField(
        max_length=50,
        null=True
    )

    FLAT_BHK_CHOICES = [
        ("Studio", "Studio"),
        ("1BHK", "1BHK"),
        ("2BHK", "2BHK"),
        ("3BHK", "3BHK"),
        ("4BHK", "4BHK"),
    ]

    flat_configuration = models.CharField(
        max_length=10,
        choices=FLAT_BHK_CHOICES,null=True
    )

    KITCHEN_TYPE_CHOICES = [
        ("Open", "Open"),
        ("Closed", "Closed"),
    ]

    FACING_CHOICES = [
        ("East", "East"),
        ("West", "West"),
        ("North", "North"),
        ("South", "South"),
    ]
    balcony = models.BooleanField(default=False,null=True)
    no_of_bathrooms = models.PositiveIntegerField(null=True)
    kitchen_type = models.CharField(
        max_length=10,
        choices=KITCHEN_TYPE_CHOICES,null=True
    )

    facing = models.CharField(
        max_length=10,
        choices=FACING_CHOICES,null=True
    )

    

    parking = models.BooleanField(default=False,null=True)
    lift = models.BooleanField(default=False,null=True)
    security = models.BooleanField(default=False,null=True)
    gas_pipeline = models.BooleanField(default=False,null=True)
    water_supply = models.BooleanField(default=False,null=True)
    intercom = models.BooleanField(default=False,null=True)
    fire_safety = models.BooleanField(default=False,null=True)

    #villa
    villa_name = models.CharField(max_length=150,null=True)
    project_name = models.CharField(
        max_length=150,
        blank=True,null=True
    )

    VILLA_TYPE_CHOICES = [
        ("Independent", "Independent"),
        ("Duplex", "Duplex"),
        ("Triplex", "Triplex"),
    ]
    villa_type = models.CharField(
        max_length=20,
        choices=VILLA_TYPE_CHOICES,null=True
    )

    VILLA_BHK_CHOICES = [
        ("2BHK", "2BHK"),
        ("3BHK", "3BHK"),
        ("4BHK", "4BHK"),
        ("5BHK", "5BHK"),
    ]
    villa_configuration = models.CharField(
        max_length=10,
        choices=VILLA_BHK_CHOICES,null=True
    )

    plot_area_sqft = models.DecimalField(
        max_digits=10,
        decimal_places=2,null=True
    )

    number_of_bedrooms = models.PositiveIntegerField(null=True)
    number_of_bathrooms = models.PositiveIntegerField(null=True)
    living_rooms_count = models.PositiveIntegerField(null=True)
    servant_room = models.BooleanField(default=False,null=True)
    balcony_or_sitout = models.BooleanField(default=False,null=True)

    private_garden = models.BooleanField(default=False,null=True)
    terrace_access = models.BooleanField(default=False,null=True)
    boundary_wall = models.BooleanField(default=False,null=True)
    driveway = models.BooleanField(default=False,null=True)

    PARKING_TYPE_CHOICES = [
        ("Open", "Open"),
        ("Covered", "Covered"),
        ("Both", "Both"),
    ]
    private_parking = models.CharField(
        max_length=10,
        choices=PARKING_TYPE_CHOICES,null=True
    )

    MAINTENANCE_TYPE_CHOICES = [
        ("Monthly", "Monthly"),
        ("Yearly", "Yearly"),
    ]
    villa_maintenance_charge_type = models.CharField(
        max_length=20,
        choices=MAINTENANCE_TYPE_CHOICES,null=True
    )
    gardening_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    water_supply_24x7 = models.BooleanField(default=False,null=True)
    security_guard = models.BooleanField(default=False,null=True)
    clubhouse_access = models.BooleanField(default=False,null=True)
    gym = models.BooleanField(default=False,null=True)
    childrens_play_area = models.BooleanField(default=False,null=True)
    internal_roads = models.BooleanField(default=False,null=True)
    street_lights = models.BooleanField(default=False,null=True)
    gated_community = models.BooleanField(default=False,null=True)

    bachelor_allowed = models.BooleanField(default=False,null=True)
    pets_allowed = models.BooleanField(default=False,null=True)


    #commercial & flat
    floor_number = models.IntegerField(null=True,blank=True)

    #flat and villa
    power_backup = models.BooleanField(default=False,null=True)
    cctv = models.BooleanField(default=False,null=True)
    allowed_tenant_types = models.JSONField(
        default=list,
        help_text="Example: ['Bachelor', 'Family']",null=True
    )
    store_room = models.BooleanField(default=False,null=True)

    #commercial and villa
    maintenance_charge_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )
    
    # Commercial charge amounts
    electricity_charge_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    water_charge_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        db_table = "property_detail"
        ordering = ["-created_at"]

    def __str__(self):
        return f"PropertyDetail {self.property_detail_id} - {self.building_name}"

    @staticmethod
    def create(
        property_id: int,
        building_name: str,
        total_floors: int,
        carpet_area_sqft: float,
        builtup_area_sqft: float,
        monthly_rent: float,
        security_deposit_amount: float,
        late_fee_type: str,
        late_fee_value: float,
        current_status: str,
        landlord_id: int,
        created_by_id: int,
        address_line_1: str,
        area_zone: str,
        city: str,
        state: str,
        country: str,
        pincode: str,
        google_map_location: str,
        year_of_construction: int,
        address_line_2: str,
        internal_notes: str,
        electricity_charge_type: str = None,
        water_charge_type: str = None,
        other_charges: dict = None,
        available_from = None,
        current_tenant_id: int = None,
        # Flat-specific fields
        flat_number: str = None,
        floor_number: int = None,
        building_block: str = None,
        flat_configuration: str = None,
        no_of_bathrooms: int = None,
        kitchen_type: str = None,
        facing: str = None,
        balcony: bool = None,
        parking: bool = None,
        lift: bool = None,
        security: bool = None,
        gas_pipeline: bool = None,
        water_supply: bool = None,
        intercom: bool = None,
        fire_safety: bool = None,
        power_backup: bool = None,
        cctv: bool = None,
        allowed_tenant_types: list = None,
        store_room: bool = None,
        # Commercial-specific fields
        commercial_category: str = None,
        frontage_width_ft: float = None,
        ceiling_height_ft: float = None,
        no_of_cabins: int = None,
        no_of_washrooms: int = None,
        loading_area: str = None,
        power_load_kw: float = None,
        has_dg_backup: bool = None,
        lift_type: str = None,
        fire_safety_compliant: bool = None,
        emergency_exit: bool = None,
        parking_availability: str = None,
        commercial_maintenance_charge_type: str = None,
        gst_applicable: bool = None,
        gst_percentage: float = None,
        security_deposit_months: int = None,
        lease_type: str = None,
        lease_tenure_years: int = None,
        lock_in_period_months: int = None,
        allowed_business: str = None,
        prohibited_business: str = None,
        # Villa-specific fields
        villa_name: str = None,
        villa_type: str = None,
        villa_configuration: str = None,
        project_name: str = None,
        plot_area_sqft: float = None,
        number_of_bedrooms: int = None,
        number_of_bathrooms: int = None,
        living_rooms_count: int = None,
        servant_room: bool = None,
        balcony_or_sitout: bool = None,
        private_garden: bool = None,
        terrace_access: bool = None,
        boundary_wall: bool = None,
        driveway: bool = None,
        private_parking: str = None,
        villa_maintenance_charge_type: str = None,
        gardening_charges: float = None,
        water_supply_24x7: bool = None,
        security_guard: bool = None,
        clubhouse_access: bool = None,
        gym: bool = None,
        childrens_play_area: bool = None,
        internal_roads: bool = None,
        street_lights: bool = None,
        gated_community: bool = None,
        bachelor_allowed: bool = None,
        pets_allowed: bool = None,
        # Shared fields
        maintenance_charge_amount: float = None,
        electricity_charge_amount: float = None,
        water_charge_amount: float = None,
    ) -> int:
        """Create a new PropertyDetail record."""
        # Validate foreign keys
        from pms_apps.property.models.property import Property
        from pms_apps.lead.models.lead import Lead
        from pms_apps.authentication.models import User

        # Validate foreign keys
        try:
            property_obj = Property.objects.get(property_id=property_id)
        except Property.DoesNotExist:
            raise ValueError(f"Invalid Property ID: {property_id}")

        try:
            landlord = Lead.objects.get(lead_id=landlord_id)
        except Lead.DoesNotExist:
            raise ValueError(f"Invalid Landlord ID: {landlord_id}")

        try:
            created_by = User.objects.get(user_id=created_by_id)
        except User.DoesNotExist:
            raise ValueError(f"Invalid User ID: {created_by_id}")

        if current_tenant_id:
            try:
                Lead.objects.get(lead_id=current_tenant_id)
            except Lead.DoesNotExist:
                raise ValueError(f"Invalid Tenant ID: {current_tenant_id}")

        property_detail = PropertyDetail(
            property=property_obj,
            building_name=building_name,
            total_floors=total_floors,
            year_of_construction=year_of_construction,
            carpet_area_sqft=carpet_area_sqft,
            builtup_area_sqft=builtup_area_sqft,
            monthly_rent=monthly_rent,
            security_deposit_amount=security_deposit_amount,
            electricity_charge_type=electricity_charge_type,
            water_charge_type=water_charge_type,
            other_charges=other_charges or {},
            late_fee_type=late_fee_type,
            late_fee_value=late_fee_value,
            current_status=current_status,
            available_from=available_from,
            landlord_id=landlord_id,
            current_tenant_id=current_tenant_id,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            area_zone=area_zone,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
            google_map_location=google_map_location,
            internal_notes=internal_notes,
            created_by_id=created_by_id,
            # Flat fields
            flat_number=flat_number,
            floor_number=floor_number,
            building_block=building_block,
            flat_configuration=flat_configuration,
            no_of_bathrooms=no_of_bathrooms,
            kitchen_type=kitchen_type,
            facing=facing,
            balcony=balcony,
            parking=parking,
            lift=lift,
            security=security,
            gas_pipeline=gas_pipeline,
            water_supply=water_supply,
            intercom=intercom,
            fire_safety=fire_safety,
            power_backup=power_backup,
            cctv=cctv,
            allowed_tenant_types=allowed_tenant_types or [],
            store_room=store_room,
            # Commercial fields
            commercial_category=commercial_category,
            frontage_width_ft=frontage_width_ft,
            ceiling_height_ft=ceiling_height_ft,
            no_of_cabins=no_of_cabins,
            no_of_washrooms=no_of_washrooms,
            loading_area=loading_area,
            power_load_kw=power_load_kw,
            has_dg_backup=has_dg_backup,
            lift_type=lift_type,
            fire_safety_compliant=fire_safety_compliant,
            emergency_exit=emergency_exit,
            parking_availability=parking_availability,
            commercial_maintenance_charge_type=commercial_maintenance_charge_type,
            gst_applicable=gst_applicable,
            gst_percentage=gst_percentage,
            security_deposit_months=security_deposit_months,
            lease_type=lease_type,
            lease_tenure_years=lease_tenure_years,
            lock_in_period_months=lock_in_period_months,
            allowed_business=allowed_business,
            prohibited_business=prohibited_business,
            # Villa fields
            villa_name=villa_name,
            villa_type=villa_type,
            villa_configuration=villa_configuration,
            project_name=project_name,
            plot_area_sqft=plot_area_sqft,
            number_of_bedrooms=number_of_bedrooms,
            number_of_bathrooms=number_of_bathrooms,
            living_rooms_count=living_rooms_count,
            servant_room=servant_room,
            balcony_or_sitout=balcony_or_sitout,
            private_garden=private_garden,
            terrace_access=terrace_access,
            boundary_wall=boundary_wall,
            driveway=driveway,
            private_parking=private_parking,
            villa_maintenance_charge_type=villa_maintenance_charge_type,
            gardening_charges=gardening_charges,
            water_supply_24x7=water_supply_24x7,
            security_guard=security_guard,
            clubhouse_access=clubhouse_access,
            gym=gym,
            childrens_play_area=childrens_play_area,
            internal_roads=internal_roads,
            street_lights=street_lights,
            gated_community=gated_community,
            bachelor_allowed=bachelor_allowed,
            pets_allowed=pets_allowed,
            # Shared fields
            maintenance_charge_amount=maintenance_charge_amount,
            electricity_charge_amount=electricity_charge_amount,
            water_charge_amount=water_charge_amount,
        )
        property_detail.save()
        return property_detail.property_detail_id

    @staticmethod
    def get(property_detail_id: int):
        """Get PropertyDetail by ID."""
        return PropertyDetail.objects.filter(
            property_detail_id=property_detail_id
        ).first()

    @staticmethod
    def get_by_property(property_id: int):
        """Get PropertyDetail by Property ID."""
        return PropertyDetail.objects.filter(
            property_id=property_id
        ).first()

    @staticmethod
    def get_by_properties(property_ids: list):
        """Get PropertyDetails for multiple Property IDs."""
        return PropertyDetail.objects.filter(
            property_id__in=property_ids
        )

    @staticmethod
    def update(
        property_id: int,
        **kwargs
    ) -> int:
        property_detail = PropertyDetail.objects.filter(property_id=property_id).first()
        if not property_detail:
            raise ValueError(f"PropertyDetail not found for Property ID: {property_id}")

        for key, value in kwargs.items():
            if value is not None:
                if key == 'allowed_tenant_types' and not isinstance(value, list):
                    continue # Should be a list
                setattr(property_detail, key, value)
        
        property_detail.save()
        return property_detail.property_detail_id




 
















