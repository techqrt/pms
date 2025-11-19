import json
from django.db.models import Prefetch
from pms_apps.marketing.models import MarketingManager, MarketingEmployee
from pms_apps.common.common import Common
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


