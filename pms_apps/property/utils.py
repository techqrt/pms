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
        return {field: reverse_map.get(field, '') for field in fields}

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
