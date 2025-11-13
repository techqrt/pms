import json
from django.db.models import Prefetch
from pms_apps.marketing.models import MarketingManager, MarketingEmployee
from pms_apps.common.utils import Utils
from pms_apps.common.exceptions.validation_errors import ValidationErrors


class PropertyUtils:
    def __init__(self, columns_required=None):
        self.columns_required = columns_required

    # -----------------------
    # VALIDATIONS
    # -----------------------
    @staticmethod
    def check_constraints(params):
        errors = []
        if params.dimension_length_ft and float(params.dimension_length_ft) < 0:
            errors.append("Length cannot be negative.")
        if params.dimension_breadth_ft and float(params.dimension_breadth_ft) < 0:
            errors.append("Breadth cannot be negative.")
        if params.photos and len(params.photos) > 5:
            errors.append("Maximum 5 photos allowed.")
        if params.videos and len(params.videos) > 5:
            errors.append("Maximum 5 videos allowed.")
        if errors:
            raise ValidationErrors(errors=errors)

    # -----------------------
    # EXTRACT METHODS
    # -----------------------
    @staticmethod
    def create_extract(params):
        return {
            "building_details": params.building_details,
            "floor": params.floor,
            "flat_number": params.flat_number,
            "dimension_length_ft": params.dimension_length_ft,
            "dimension_breadth_ft": params.dimension_breadth_ft,
            "dimension_area_sqft": params.dimension_area_sqft,
            "rental_type": params.rental_type,
            "hall": params.hall or False,
            "bedroom_count": params.bedroom_count or 0,
            "kitchen": params.kitchen or False,
            "attached_bathroom_count": params.attached_bathroom_count or 0,
            "single_bathroom_count": params.single_bathroom_count or 0,
            "balcony": params.balcony or False,
            "store_room": params.store_room or False,
            "rental_for": params.rental_for,
            "advance_amount_rent": params.advance_amount_rent,
            "expected_rent": params.expected_rent,
            "agreement_id": params.agreement_id,
            "photos": params.photos or [],
            "videos": params.videos or [],
            "created_by_id": getattr(params.created_by, "user_id", None),
            "assigned_to_id": getattr(params.assigned_to, "user_id", None),
        }

    @staticmethod
    def update_extract(params):
        data = {
            "building_details": params.building_details,
            "floor": params.floor,
            "flat_number": params.flat_number,
            "dimension_length_ft": params.dimension_length_ft,
            "dimension_breadth_ft": params.dimension_breadth_ft,
            "dimension_area_sqft": params.dimension_area_sqft,
            "rental_type": params.rental_type,
            "hall": params.hall,
            "bedroom_count": params.bedroom_count,
            "kitchen": params.kitchen,
            "attached_bathroom_count": params.attached_bathroom_count,
            "single_bathroom_count": params.single_bathroom_count,
            "balcony": params.balcony,
            "store_room": params.store_room,
            "rental_for": params.rental_for,
            "advance_amount_rent": params.advance_amount_rent,
            "expected_rent": params.expected_rent,
            "agreement_id": params.agreement_id,
            "photos": params.photos,
            "videos": params.videos,
            "assigned_to_id": getattr(params.assigned_to, "user_id", None),
        }
        return {k: v for k, v in data.items() if v is not None}

    # -----------------------
    # USER ROLE MAPPER
    # -----------------------
    @staticmethod
    def map_user_with_role(user):
        if not user:
            return None
        if hasattr(user, "marketing_manager_profile"):
            return {
                "user_id": user.id,
                "username": user.username,
                "role": "Marketing Manager",
                "department": user.marketing_manager_profile.department or None,
            }
        elif hasattr(user, "marketing_employee_profile"):
            return {
                "user_id": user.id,
                "username": user.username,
                "role": "Marketing Employee",
                "designation": user.marketing_employee_profile.designation or None,
            }
        return {"user_id": user.id, "username": user.username, "role": "Other"}

    # -----------------------
    # PROPERTY MAPPER
    # -----------------------
    def mapper(self, data):
        mapped = []
        for prop in data:
            mapped.append({
                "property_id": prop.property_id,
                "building_details": prop.building_details,
                "expected_rent": str(prop.expected_rent) if prop.expected_rent else None,
                "created_by": self.map_user_with_role(prop.created_by),
                "assigned_to": self.map_user_with_role(prop.assigned_to),
                "is_active": prop.is_active,
                "created_at": prop.created_at,
                "updated_at": prop.updated_at,
            })
        return json.dumps(mapped, default=str)

    # -----------------------
    # PREFETCH QUERY OPTIMIZATION
    # -----------------------
    @staticmethod
    def optimized_queryset():
        from pms_apps.property.models.property import Property
        return Property.objects.select_related("created_by", "assigned_to").prefetch_related(
            Prefetch("created_by__marketing_manager_profile", queryset=MarketingManager.objects.only("manager_id", "department")),
            Prefetch("created_by__marketing_employee_profile", queryset=MarketingEmployee.objects.only("employee_id", "designation")),
            Prefetch("assigned_to__marketing_manager_profile", queryset=MarketingManager.objects.only("manager_id", "department")),
            Prefetch("assigned_to__marketing_employee_profile", queryset=MarketingEmployee.objects.only("employee_id", "designation")),
        ).filter(is_active=True).order_by("-created_at")
