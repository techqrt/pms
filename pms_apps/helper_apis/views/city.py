from pms_apps.common.common import Common
from pms_apps.common.dataclasses.request.get_all import GetAll
from rest_framework.response import Response
from django.db import transaction
from django.core.paginator import Paginator
from pms_apps.helper_apis.utils.city import CityUtils
from pms_apps.helper_apis.serilizers.city.response.get_all import CityResponseGetAllSerializer
import json
from pms_apps.common.utils import Utils
from rest_framework import status
from pms_apps.helper_apis.models.city import City


class CityView:
    def __init__(self):
        self.data_create = "Added successfully"
        self.data_update = "Updated successfully"
        self.data_delete =  "Deleted successfully"
        self.data_no_match = "No matching entry found"
        self.data_get = "Data fetched successfully"
        self.db_error = "Database Error"
        self.error = "Something went wrong"

    @Common(response_handler=CityResponseGetAllSerializer).exception_handler
    def get_all(self,params : GetAll):
        with transaction.atomic():

            reversed_mapped = CityUtils.reverse_mapper([
                params.filter_key
            ])
            pages = Paginator(City.get_all(
                search_key=params.search_key,
                filter_key=reversed_mapped.get(params.filter_key),
                filter_value=params.filter_value
            ),per_page=params.limit)
    

            if pages.num_pages < params.page_num:
                raise ValueError('Page limit exceed!')
                
            data = pages.page(params.page_num)
            lead_utils = CityUtils(columns_required=[column for column in params.values.split(',') if column])
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
    
    