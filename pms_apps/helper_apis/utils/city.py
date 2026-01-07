import pandas
from pms_apps.common.common import Common
import json

class CityUtils:
    def __init__(self, columns_required: list = []) -> None:
        self.columns_required = columns_required
        self.mapped_columns_name = {
            'city_id' : 'cityId',
            'name' : 'name',
            'country__name' : 'countryName',
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
        reverse_map = {v: k for k, v in CityUtils().mapped_columns_name.items()}
        return {field: reverse_map.get(field,'') for field in fields}
