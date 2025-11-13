from drf_spectacular.utils import OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from pms.config import Configurations
from pms.constants import Constants
from pms_apps.common.utils import Utils


class SwaggerPage:
    
    @staticmethod
    def response(description="Success", response=None):
        return {200: OpenApiResponse(description=description, response=response)}
    
    @staticmethod
    def get_all_parameters():
        return [
            OpenApiParameter(name='value', description='column required with coma separated',
                             required=False, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
            OpenApiParameter(name='page_num', description='page number to get the list of records',
                             required=False, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
            OpenApiParameter(name='limit', description='number of data in a single page', required=False,
                             type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                             default=Configurations.pagination_count),
            OpenApiParameter(name='sort_by', description='Field to sort by', required=False,
                             type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, default='name'),
            OpenApiParameter(name='sort_order', description='Sort by Ascending or Descending',
                             required=False,
                             location=OpenApiParameter.QUERY,
                             type=str, enum=['asc', 'desc']),
            OpenApiParameter(name='filter_key', description='Field to filter by (e.g., "is_active")',
                             required=False,
                             location=OpenApiParameter.QUERY,
                             type=str, enum=['is_active']
            ),
            OpenApiParameter(name='filter_value', description='Value for the filter field (e.g., "true" or "false" for "is_active")',
                             required=False,
                             location=OpenApiParameter.QUERY,
                             type=str, enum=['true','false']),
            OpenApiParameter(name='search_key', description='Field to search by (e.g., "name")',required=False,location=OpenApiParameter.QUERY,type=str)

        ]
    
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(name='value', description='column required with coma separated',
                             required=False, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY)
        ]
    @staticmethod
    def search_parameters(key_description):
        return [
            OpenApiParameter(name="query", description=key_description, required=True, type=str)
        ]
