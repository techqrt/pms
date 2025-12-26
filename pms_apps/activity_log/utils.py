from pms_apps.activity_log.models.activity_log import ActivityLog
from pms_apps.activity_log.models.archive_log import ArchiveLog
from datetime import timedelta
from django.utils import timezone
import pandas
import json
from pms_apps.common.common import Common


class ActivityLogUtils:
    def __init__(self, columns_required: list = []) -> None:
        self.columns_required = columns_required
        self.mapped_columns_name = {
            "log_id" : "logId",
            "user__user_id" : "user.userId",
            "user__name" : "user.name",
            "user__phone_number" : "user.phoneNumber",
            "user__email" : "user.email",
            "ip_address" : "ipAddress",
            "user_agent" : "userAgent",
            "action" : "action",
            "model" : "model",
            "method" : "method",
            "end_point" : "endPoint",
            "details" : "details",
            "created_on" : "createdOn",
            
        }
        self.include_log_fields = {
            'lead' : ('lead_id','first_name','last_name')
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
        reverse_map = {v: k for k, v in ActivityLogUtils().mapped_columns_name.items()}
        return {field: reverse_map.get(field,'') for field in fields}

    @staticmethod
    def create_activity_event(
        user_id: int,
        ip_address: str,
        user_agent: str,
        action: str,
        model: str,
        method: str,
        end_point: str,
        details : dict
    ):
        ActivityLog.objects.create(
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            action=action,
            model=model,
            method=method,
            end_point=end_point,
            details = details,
        )
        time_threshold = timezone.now() - timedelta(hours=24)
        old_logs = ActivityLog.objects.filter(created_on__lt=time_threshold)

        if old_logs.exists():
            ArchiveLog.objects.bulk_create([
                ArchiveLog(
                    log_id = log.log_id,
                    user=log.user,
                    ip_address=log.ip_address,
                    user_agent=log.user_agent,
                    action=log.action,
                    model=log.model,
                    method=log.method,
                    end_point=log.end_point,
                    details = details,
                    created_on =log.created_on,
                )
                for log in old_logs
            ])

            old_logs.delete()

    def get_log_include_fields(
            self,
            model_name : str
        ) -> tuple | None:
        return self.include_log_fields.get(model_name,None)

