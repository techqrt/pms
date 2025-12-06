import json
from django.db.models import Prefetch
from pms_apps.common.common import Common
from pms_apps.marketing.models.marketing_employee import MarketingEmployee
from pms_apps.marketing.models.marketing_manager import MarketingManager
from pms_apps.common.utils import Utils
from pms_apps.common.exceptions.validation_errors import ValidationErrors
import pandas

class PropertyUtils:
    def __init__(self, columns_required=None):
        self.columns_required = columns_required
        self.mapped_columns_name = {
            'property_id': 'propertyId',
            'block' : 'block',
            'building_details': 'buildingDetails',
            'floor': 'floor',
            'flat_number': 'flatNumber',
            'dimension_length_ft': 'dimensionLengthFt',
            'dimension_breadth_ft': 'dimensionBreadthFt',
            'dimension_area_sqft': 'dimensionAreaSqft',
            'rental_type': 'rentalType',
            'hall': 'hall',
            'bedroom_count': 'bedroomCount',
            'kitchen': 'kitchen',
            'attached_bathroom_count': 'attachedBathroomCount',
            'single_bathroom_count': 'singleBathroomCount',
            'balcony': 'balcony',
            'store_room': 'storeRoom',
            'rental_for': 'rentalFor',
            'advance_amount_rent': 'advanceAmountRent',
            'expected_rent': 'expectedRent',
            'agreement_id': 'agreementId',
            'photos': 'photos',
            'videos': 'videos',
            'created_by__user_id': 'createdBy.userId',
            'created_by__name': 'createdBy.name',
            'created_by__phone_number': 'createdBy.phoneNumber',
            'created_by__email': 'createdBy.email',
            'assigned_to__user_id': 'assignedTo.userId',
            'assigned_to__name': 'assignedTo.name',
            'assigned_to__phone_number': 'assignedTo.phoneNumber',
            'assigned_to__email': 'assignedTo.email',
            'created_at': 'createdAt',
            'updated_at': 'updatedAt',
            'is_active': 'isActive'
        }

    @staticmethod
    def flatten_to_nested_dict(df):
        result = []

        import numpy as np

        df = df.applymap(lambda x: x.isoformat() if isinstance(x, pandas.Timestamp) else (None if pandas.isna(x) else x))
        df = df.replace({np.nan: None, np.inf: None, -np.inf: None})

        for _, row in df.iterrows():
            row_dict = {}
            for col, val in row.items():
                if "." in col:
                    parts = col.split(".")
                    current = row_dict
                    for part in parts[:-1]:
                        current = current.setdefault(part, {})
                    current[parts[-1]] = val
                else:
                    row_dict[col] = val
            result.append(row_dict)

        return result, df

    def mapper(self, data: list) -> str | None:
        if not data:
            return '[]'

        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_columns_name, inplace=True)

        if self.columns_required:
            Common.mapper_value_error(
                mapped_column_names=self.mapped_columns_name,
                columns_required=self.columns_required
            )

            dataframe = dataframe[self.columns_required]

        flatten_data, cleaned_df = self.flatten_to_nested_dict(dataframe)
        return json.dumps(flatten_data, default=str)

    @staticmethod
    def reverse_mapper(fields: list[str]) -> dict[str, str]:
        reverse_map = {v: k for k, v in PropertyUtils().mapped_columns_name.items()}
        return {field: reverse_map.get(field, '') for field in fields}


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
            Prefetch("created_by__marketing_manager_profile",
                     queryset=MarketingManager.objects.only("manager_id", "department")),
            Prefetch("created_by__marketing_employee_profile",
                     queryset=MarketingEmployee.objects.only("employee_id", "designation")),
            Prefetch("assigned_to__marketing_manager_profile",
                     queryset=MarketingManager.objects.only("manager_id", "department")),
            Prefetch("assigned_to__marketing_employee_profile",
                     queryset=MarketingEmployee.objects.only("employee_id", "designation")),
        ).filter(is_active=True).order_by("-created_at")
