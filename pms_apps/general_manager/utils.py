import pandas
from pms_apps.common.common import Common
import json

class GeneralManagerUtils:
    def __init__(self, entity: str, columns_required: list = []) -> None:
        self.columns_required = columns_required
        self.entity = entity  # 'general manager'

        general_manager_map = {
            'general_manager_id': 'generalManagerId',
            'general_manager_id__phone_number': 'phoneNumber',
            'general_manager_id__email': 'email',
            'name': 'name',
            'dob': 'dob',
            'department': 'department',
            'years_of_experience': 'yearsOfExperience',
            'created_at': 'createdAt',
        }

        self.mapped_columns_name = general_manager_map if entity == 'general manager' else {}

    @staticmethod
    def flatten_to_nested_dict(df):
        result = []

        import numpy as np

        df = df.applymap(lambda x: x.isoformat() if isinstance(
            x, pandas.Timestamp) else (None if pandas.isna(x) else x))
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

        flatten_data, _ = self.flatten_to_nested_dict(dataframe)
        return json.dumps(flatten_data, default=str)

    @staticmethod
    def reverse_mapper(fields: list[str]) -> dict[str, str]:
        combined_map = {}
        combined_map.update(GeneralManagerUtils('general_manager').mapped_columns_name)
        reverse_map = {v: k for k, v in combined_map.items()}
        return {field: reverse_map.get(field, '') for field in fields}
