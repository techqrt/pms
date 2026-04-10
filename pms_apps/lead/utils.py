import pandas
from pms_apps.common.common import Common
import json

class LeadUtils:
    def __init__(self, columns_required: list = []) -> None:
        self.columns_required = columns_required
        self.mapped_columns_name = {
            'lead_id': 'leadId',
            'first_name': 'firstName',
            'last_name': 'lastName',
            'lead_category': 'leadCategory',
            'lead_origin': 'leadOrigin',
            'address': 'address',
            'po_box': 'poBox',
            'feedback': 'feedback',
            'country__name' : 'country',
            'city__name' : 'city',
            'nationality__name' : 'nationality',
            'passport_or_id': 'passportOrId',
            'purpose': 'purpose',
            'created_at': 'createdAt',
            'updated_at': 'updatedAt',
            'is_active': 'isActive',
            'lead_assign_to__name': 'leadAssignTo.name',
            'lead_assign_to__user_id': 'leadAssignTo.userId',
            'lead_assign_to__phone_number': 'leadAssignTo.phoneNumber',
            'lead_assign_to__email': 'leadAssignTo.email',
            'lead_id__phone_number': 'phoneNumber',
            'property_permissions__permission_id' : 'propertyPermission.permissionId',
            'property_permissions__property' : 'propertyPermission.property',
            'profile_image': 'profileImage'
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

        if self.columns_required:
            Common.mapper_value_error(
                mapped_column_names=self.mapped_columns_name,
                columns_required=self.columns_required
            )
            # Map required columns back to DB names for filtering before rename
            reverse_map = {v: k for k, v in self.mapped_columns_name.items()}
            db_columns = [reverse_map.get(col, col) for col in self.columns_required]
            # Filter dataframe using DB column names
            dataframe = dataframe[db_columns]

        dataframe.rename(columns=self.mapped_columns_name, inplace=True)

        flatten_data, cleaned_df = self.flatten_to_nested_dict(dataframe)
        return json.dumps(flatten_data, default=str)
    
    @staticmethod
    def reverse_mapper(fields: list[str]) -> dict[str, str]:
        reverse_map = {v: k for k, v in LeadUtils().mapped_columns_name.items()}
        return {field: reverse_map.get(field,'') for field in fields}
