from django.db import models
from django.contrib.postgres.fields import ArrayField
from pms_apps.authentication.models import User
from django.db.models import Q


class Property(models.Model):
    RENTAL_TYPE_CHOICES = [
        ("Flat", "Flat"),
        ("Commercial", "Commercial"),
        ("Villa","Villa"),
        ("Warehouse", "Warehouse")
    ]

    RENTAL_FOR_CHOICES = [
        ("Bachelor", "Bachelor"),
        ("Family", "Family"),
        ("Labour", "Labour"),
    ]

    property_id = models.AutoField(primary_key=True)
    building = models.ForeignKey(
        "property.Building", on_delete=models.PROTECT, null=True, blank=True,
        related_name="units"
    )
    block = models.CharField(max_length=50, null=True, blank=True)
    building_details = models.CharField(max_length=255, null=True, blank=True)
    floor = models.CharField(max_length=50, null=True, blank=True)
    flat_number = models.IntegerField(null=True, blank=True)

    dimension_length_ft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dimension_breadth_ft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dimension_area_sqft = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    rental_type = models.CharField(max_length=20, choices=RENTAL_TYPE_CHOICES, default="Residential")

    rental_for = models.CharField(max_length=20, choices=RENTAL_FOR_CHOICES, default="Family")

    advance_amount_rent = models.IntegerField(null=True, blank=True)
    expected_rent = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    agreement_id = models.PositiveIntegerField(null=True, blank=True)

    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="property_created_by"
    )
    assigned_to = models.ManyToManyField(
        User, related_name="property_assigned_to", blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "property"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Property {self.property_id} - {self.building_details or 'N/A'}"


    def create(
        self,
        block: str,
        building_details: str,
        floor: str,
        flat_number: int,
        dimension_length_ft: float,
        dimension_breadth_ft: float,
        dimension_area_sqft: float,
        rental_type: str,
        rental_for: str,
        advance_amount_rent: int,
        expected_rent: float,
        agreement_id: int,
        created_by: int,
        building_id: int = None,
    ) -> int:
        self.building_id = building_id
        self.block = block
        self.building_details = building_details
        self.floor = floor
        self.flat_number = flat_number
        self.dimension_length_ft = dimension_length_ft
        self.dimension_breadth_ft = dimension_breadth_ft
        self.dimension_area_sqft = dimension_area_sqft
        self.rental_type = rental_type
        self.rental_for = rental_for
        self.advance_amount_rent = advance_amount_rent
        self.expected_rent = expected_rent
        self.agreement_id = agreement_id
        self.created_by_id = created_by

        self.save()
        return self.property_id



    @staticmethod
    def update(
        property_id: int,
        block: str = None,
        building_details: str = None,
        floor: str = None,
        flat_number: int = None,
        dimension_length_ft: float = None,
        dimension_breadth_ft: float = None,
        dimension_area_sqft: float = None,
        rental_type: str = None,
        rental_for: str = None,
        advance_amount_rent: int = None,
        expected_rent: float = None,
        agreement_id: int = None,
        assigned_to: list = None,
        building_id: int = None,
    ) -> int:
        try:
            property = Property.objects.get(property_id=property_id)
        except Property.DoesNotExist:
            raise ValueError(f"Invalid Property Id: {property_id}")

        if building_id is not None:
            property.building_id = building_id
        if block is not None:
            property.block = block
        if building_details is not None:
            property.building_details = building_details
        if floor is not None:
            property.floor = floor
        if flat_number is not None:
            property.flat_number = flat_number
        if dimension_length_ft is not None:
            property.dimension_length_ft = dimension_length_ft
        if dimension_breadth_ft is not None:
            property.dimension_breadth_ft = dimension_breadth_ft
        if dimension_area_sqft is not None:
            property.dimension_area_sqft = dimension_area_sqft
        if rental_type is not None:
            property.rental_type = rental_type
        if rental_for is not None:
            property.rental_for = rental_for
        if advance_amount_rent is not None:
            property.advance_amount_rent = advance_amount_rent
        if expected_rent is not None:
            property.expected_rent = expected_rent
        if agreement_id is not None:
            property.agreement_id = agreement_id

        property.save()

        if assigned_to is not None:
            property.assigned_to.set(assigned_to)

        return property.property_id



    @staticmethod
    def get(property_id):
        """Get property by ID."""
        return Property.objects.filter(
            property_id=property_id,
            is_active=True
        ).values(
            'property_id','building_id','building__name','block','building_details','floor','flat_number',
            'dimension_length_ft','dimension_breadth_ft','dimension_area_sqft','rental_type','rental_for','advance_amount_rent','expected_rent','agreement_id','created_by__user_id','created_by__name','created_by__phone_number','created_by__email','created_at','updated_at','is_active'
        ).first()


    @staticmethod
    def get_all(
        sort_by: str = '',
        sort_order: str = '',
        filter_key: str = '',
        filter_value: str = '',
        search_key: str = '',
    ) -> list:
        data = Property.objects.filter(is_active=True)

        if filter_key and filter_value:
            data = data.filter(**{filter_key+"__icontains": filter_value})

        if search_key:
            data = data.filter(
                Q(building_details__icontains=search_key) |
                Q(block__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")
        else:
            data = data.order_by("-created_at")

        data = data.values(
            'property_id','building_id','building__name','block','building_details','floor','flat_number',
            'dimension_length_ft','dimension_breadth_ft','dimension_area_sqft','rental_type','rental_for','advance_amount_rent','expected_rent','agreement_id','created_by__user_id','created_by__name','created_by__phone_number','created_by__email','created_at','updated_at','is_active'
        )

        return list(data)


    @staticmethod
    def delete(property_id):
        return Property.objects.filter(property_id=property_id).update(is_active=False)

    @staticmethod
    def delete_many(ids: list):
        """Soft delete multiple properties by IDs."""
        return Property.objects.filter(property_id__in=ids).update(is_active=False)

    @staticmethod
    def get_all_by_user(
        user_id: int,
        sort_by: str = '',
        sort_order: str = '',
        filter_key: str = '',
        filter_value: str = '',
        search_key: str = '',
        property_types: list = None,
        rental_for: list = None,
        bedrooms: list = None,
        features: list = None,
        building_id: int = None,
        city: str = '',
        min_rent=None,
        max_rent=None,
        from_date=None,
        to_date=None,
    ) -> list:
        TYPE_ALIAS_TO_DB = {"Apartment": "Flat"}
        FEATURE_FILTERS = {
            "Balcony": Q(propertydetail__balcony=True) | Q(propertydetail__balcony_or_sitout=True),
            "Parking": Q(propertydetail__parking=True),
            "Pool": ~Q(propertydetail__swimming_pool="No") & Q(propertydetail__swimming_pool__isnull=False),
        }

        data = Property.objects.filter(
            is_active=True
        ).filter(
            Q(created_by__user_id=user_id) |
            Q(assigned_to__user_id=user_id) |
            Q(propertydetail__landlord__lead_id__user_id=user_id)
        ).distinct()

        if filter_key and filter_value:
            data = data.filter(**{filter_key: filter_value})

        if building_id:
            data = data.filter(building_id=building_id)

        if property_types:
            db_types = [TYPE_ALIAS_TO_DB.get(t, t) for t in property_types]
            data = data.filter(rental_type__in=db_types)

        if rental_for:
            data = data.filter(rental_for__in=rental_for)

        if bedrooms:
            data = data.filter(
                Q(propertydetail__flat_configuration__in=bedrooms) |
                Q(propertydetail__villa_configuration__in=bedrooms)
            )

        if features:
            feature_filter = Q()
            for feature in features:
                if feature in FEATURE_FILTERS:
                    feature_filter |= FEATURE_FILTERS[feature]
            if feature_filter:
                data = data.filter(feature_filter)

        if city:
            data = data.filter(propertydetail__city__icontains=city)

        if min_rent is not None:
            data = data.filter(expected_rent__gte=min_rent)
        if max_rent is not None:
            data = data.filter(expected_rent__lte=max_rent)

        if from_date:
            data = data.filter(created_at__gte=from_date)
        if to_date:
            data = data.filter(created_at__lte=to_date)

        if search_key:
            data = data.filter(
                Q(building_details__icontains=search_key) |
                Q(block__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")
        else:
            data = data.order_by("-created_at")

        data = data.values(
            'property_id','building_id','building__name','block','building_details','floor','flat_number',
            'dimension_length_ft','dimension_breadth_ft','dimension_area_sqft','rental_type','rental_for','advance_amount_rent','expected_rent','agreement_id','created_by__user_id','created_by__name','created_by__phone_number','created_by__email','created_at','updated_at','is_active'
        )

        return list(data)

    @staticmethod
    def get_assignees_map(property_ids: list) -> dict:
        """Bulk-fetch assigned users per property_id, keyed as {property_id: [user_dict, ...]}."""
        from collections import defaultdict
        rows = Property.assigned_to.through.objects.filter(
            property_id__in=property_ids
        ).values('property_id', 'user__user_id', 'user__name', 'user__phone_number', 'user__email')
        result = defaultdict(list)
        for row in rows:
            result[row['property_id']].append({
                'userId': row['user__user_id'],
                'name': row['user__name'],
                'phoneNumber': row['user__phone_number'],
                'email': row['user__email'],
            })
        return result

class CommercialProperty(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, primary_key=True)
    commercial_type = models.CharField(max_length=100, null=True, blank=True) 
    
     # e.g., Office, Retail, Industrial

    class Meta:
        db_table = "commercial_property"

    def __str__(self):
        return f"Commercial Property {self.property.property_id} - {self.commercial_type or 'N/A'}" 