from drf_spectacular.utils import extend_schema
from pms_apps.common.swagger import SwaggerPage
from rest_framework.decorators import api_view
from pms_apps.common.serializer_validations import SerializerValidations
from rest_framework.response import Response
from pms_apps.common.serializers.request.get_all import  GetAllSerializer
from pms_apps.helper_apis.views.city import CityView
from pms_apps.helper_apis.serilizers.city.response.get_all import CityResponseGetAllSerializer


class CityViewController:
    @extend_schema(
        description="Get all Cities",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=CityResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request:Response) -> Response:
        return CityView().get_all(params=request.params)