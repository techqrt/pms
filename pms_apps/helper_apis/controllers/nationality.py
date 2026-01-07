from drf_spectacular.utils import extend_schema
from pms_apps.common.swagger import SwaggerPage
from rest_framework.decorators import api_view
from pms_apps.common.serializer_validations import SerializerValidations
from rest_framework.response import Response
from pms_apps.common.serializers.request.get_all import  GetAllSerializer
from pms_apps.helper_apis.serilizers.nationality.response.get_all import NationalityResponseGetAllSerilizers
from pms_apps.helper_apis.views.nationality import NationalityView

class NationalityController:
    @extend_schema(
        description="Get all Nationalities",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=NationalityResponseGetAllSerilizers)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request:Response) -> Response:
        return NationalityView().get_all(params=request.params)
    