from drf_spectacular.utils import extend_schema
from pms_apps.common.swagger import SwaggerPage
from rest_framework.decorators import api_view
from pms_apps.common.serializer_validations import SerializerValidations
from rest_framework.response import Response
from pms_apps.common.serializers.request.get_all import  GetAllSerializer
from pms_apps.helper_apis.serilizers.country.response.get_all import CountryResponseGetAllSerilizers
from pms_apps.helper_apis.views.country import CountryView

class CountryViewController:
    @extend_schema(
        description="Get all Countries",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=CountryResponseGetAllSerilizers)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request:Response) -> Response:
        return CountryView().get_all(params=request.params)
    

    