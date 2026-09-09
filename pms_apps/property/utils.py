import json
from django.db.models import Prefetch, Q
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
            'building_id': 'buildingId',
            'building__name': 'buildingName',
            'block': 'block',
            'building_details': 'buildingDetails',
            'floor': 'floor',
            'flat_number': 'flatNumber',
            'dimension_length_ft': 'dimensionLengthFt',
            'dimension_breadth_ft': 'dimensionBreadthFt',
            'dimension_area_sqft': 'dimensionAreaSqft',
            'rental_type': 'rentalType',
            'rental_for': 'rentalFor',
            'advance_amount_rent': 'advanceAmountRent',
            'expected_rent': 'expectedRent',
            'agreement_id': 'agreementId',
            'created_by__user_id': 'createdBy.userId',
            'created_by__name': 'createdBy.name',
            'created_by__phone_number': 'createdBy.phoneNumber',
            'created_by__email': 'createdBy.email',
            'created_at': 'createdAt',
            'updated_at': 'updatedAt',
            'is_active': 'isActive',
            'landlord_id': 'landlordId',
            'current_tenant_id': 'currentTenantId'
        }

    @staticmethod
    def get_marketing_role(user_id: int) -> str | None:
        """Returns 'Manager'/'Employee' if the user has a Marketing profile, else None."""
        if MarketingManager.get_id(user_id):
            return 'Manager'
        if MarketingEmployee.objects.filter(employee_id=user_id).exists():
            return 'Employee'
        return None

    @staticmethod
    def get_restricted_role(user_id: int) -> str | None:
        """Returns 'Manager'/'Employee' if the user belongs to Marketing or
        Check-In Check-Out - the two departments whose property/lead edit
        access is scoped by assignment (created_by/assigned_to). Every other
        department's access to these endpoints is unaffected by this check."""
        role = PropertyUtils.get_marketing_role(user_id)
        if role:
            return role
        from pms_apps.checkin_checkout.authorization import get_check_in_check_out_role
        return get_check_in_check_out_role(user_id)

    @staticmethod
    def can_employee_edit_property(property_id: int, user_id: int) -> bool:
        """A Marketing/Check-In Check-Out Employee may edit or delete a
        property they created OR are an assigned handler of
        (Property.assigned_to) - the same ownership rule applies to both
        actions. Managers and other departments are unrestricted."""
        if PropertyUtils.get_restricted_role(user_id) != 'Employee':
            return True

        from pms_apps.property.models.property import Property
        return Property.objects.filter(
            property_id=property_id
        ).filter(
            Q(created_by__user_id=user_id) | Q(assigned_to__user_id=user_id)
        ).exists()

    @staticmethod
    def can_assign_property_to_tenant(property_id: int, tenant_id: int, user_id: int) -> bool:
        """A Marketing/Check-In Check-Out Employee may only link a property to
        a tenant when they are the assigned handler for BOTH that property
        (Property.assigned_to) and that tenant (Lead.lead_assign_to). Managers
        and other departments are unrestricted, consistent with every other
        property/lead rule."""
        if PropertyUtils.get_restricted_role(user_id) != 'Employee':
            return True

        from pms_apps.property.models.property import Property
        from pms_apps.lead.models.lead import Lead

        is_assigned_to_property = Property.objects.filter(
            property_id=property_id, assigned_to__user_id=user_id
        ).exists()
        is_assigned_to_tenant = Lead.objects.filter(
            lead_id=tenant_id, lead_assign_to_id=user_id
        ).exists()
        return is_assigned_to_property and is_assigned_to_tenant

    @staticmethod
    def redact_landlord_for_employee(landlord: dict | None, landlord_assign_to_id, user_id: int) -> dict | None:
        """Marketing/Check-In Check-Out Employees see only the landlord's name
        unless that landlord is assigned to them (lead_assign_to == user_id),
        in which case they get full contact details, same as Managers and
        other departments."""
        if not landlord:
            return landlord
        if PropertyUtils.get_restricted_role(user_id) == 'Employee' and landlord_assign_to_id != user_id:
            return {**landlord, 'phoneNumber': None, 'email': None}
        return landlord

    @staticmethod
    def flatten_to_nested_dict(df):
        result = []

        import numpy as np
        
        # Convert to string to avoid issues, but handle None
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
        
        # Filter dropped columns if they exist in mapped_columns_name but not in dataframe
        actual_mapped_columns = {k: v for k, v in self.mapped_columns_name.items() if k in dataframe.columns}
        dataframe.rename(columns=actual_mapped_columns, inplace=True)

        if self.columns_required:
            Common.mapper_value_error(
                mapped_column_names=self.mapped_columns_name,
                columns_required=self.columns_required
            )
            # Only select columns that exist in the dataframe
            valid_cols = [col for col in self.columns_required if col in dataframe.columns]
            dataframe = dataframe[valid_cols]

        flatten_data, cleaned_df = self.flatten_to_nested_dict(dataframe)
        
        # Remove top-level nulls to clean up the response
        cleaned_data = [
            {k: v for k, v in item.items() if v is not None}
            for item in flatten_data
        ]
        
        return json.dumps(cleaned_data, default=str)

    @staticmethod
    def reverse_mapper(fields: list[str]) -> dict[str, str]:
        reverse_map = {v: k for k, v in PropertyUtils().mapped_columns_name.items()}
        
        # Handle common aliases for property_type and rental_for
        aliases = {
            'property_type': 'rental_type',
            'propertyType': 'rental_type',
            'purpose': 'rental_for',
            'rentalFor': 'rental_for',
        }
        
        result = {}
        for field in fields:
            if field in aliases:
                result[field] = aliases[field]
            else:
                result[field] = reverse_map.get(field, '')
        return result

    @staticmethod
    def check_constraints(params):
        errors = []
        if getattr(params, 'dimension_length_ft', None) and float(params.dimension_length_ft) < 0:
            errors.append("Length cannot be negative.")
        if getattr(params, 'dimension_breadth_ft', None) and float(params.dimension_breadth_ft) < 0:
            errors.append("Breadth cannot be negative.")
        if getattr(params, 'photos', None) and len(params.photos) > 5:
            errors.append("Maximum 5 photos allowed.")
        if getattr(params, 'videos', None) and len(params.videos) > 10: # Increased limit or stick to 5
             errors.append("Maximum 10 videos allowed.")
        if errors:
            raise ValidationErrors(errors=errors)
