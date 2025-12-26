from django.shortcuts import render
from pms_apps.common.common import Common
from pms_apps.common.dataclasses.request.get_all import GetAll
from pms_apps.activity_log.serializer.response.get_all_admin import ActivityLogAdminResponseGetAllSerilizer
from pms_apps.activity_log.serializer.response.get_all_user import ActivityLogUserResponseGetAllSerilizer
from django.db import transaction
from pms_apps.activity_log.utils import ActivityLogUtils
from django.core.paginator import Paginator
from pms_apps.activity_log.models.activity_log import ActivityLog
import json
from pms_apps.common.utils import Utils
from rest_framework.response import Response
from rest_framework import status

class ActivityLogView:
    def __init__(self):
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common(response_handler=ActivityLogUserResponseGetAllSerilizer).exception_handler
    def get_all_user(self,params : GetAll):
        with transaction.atomic():
             reversed_mapped = ActivityLogUtils.reverse_mapper([
                params.sort_by,
                params.filter_key
            ])

        pages = Paginator(ActivityLog.get_for_user(
                user_id=params.user_id,
                sort_by=reversed_mapped.get(params.sort_by),
                sort_order=params.sort_order,
                filter_key=reversed_mapped.get(params.filter_key),
                filter_value=params.filter_value,
                search_key=params.search_key
        ),per_page=params.limit)

        if pages.num_pages < params.page_num:
                raise ValueError('Page limit exceed!')
                
        data = pages.page(params.page_num)
        lead_utils = ActivityLogUtils(columns_required=[column for column in params.values.split(',') if column])
        data = json.loads(lead_utils.mapper(data=data))

        data = Utils.add_page_parameter(
                final_data=data,
                page_num=params.page_num,
                total_page=pages.num_pages,
                present_url=params.present_url,
                next_page_required=True if pages.num_pages != params.page_num else False)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )

    @Common(response_handler=ActivityLogAdminResponseGetAllSerilizer).exception_handler
    def get_all_admin(self,params : GetAll):
        with transaction.atomic():
             reversed_mapped = ActivityLogUtils.reverse_mapper([
                params.sort_by,
                params.filter_key
            ])

        pages = Paginator(ActivityLog.get_for_admin(
                sort_by=reversed_mapped.get(params.sort_by),
                sort_order=params.sort_order,
                filter_key=reversed_mapped.get(params.filter_key),
                filter_value=params.filter_value,
                search_key=params.search_key,
                from_date=params.from_date,
                to_date=params.to_date
        ),per_page=params.limit)

        if pages.num_pages < params.page_num:
                raise ValueError('Page limit exceed!')
                
        data = pages.page(params.page_num)
        lead_utils = ActivityLogUtils(columns_required=[column for column in params.values.split(',') if column])
        data = json.loads(lead_utils.mapper(data=data))

        data = Utils.add_page_parameter(
                final_data=data,
                page_num=params.page_num,
                total_page=pages.num_pages,
                present_url=params.present_url,
                next_page_required=True if pages.num_pages != params.page_num else False)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )