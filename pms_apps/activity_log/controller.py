from drf_spectacular.utils import extend_schema
from pms_apps.common.swagger import SwaggerPage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pms_apps.common.serializers.request.get_all import  GetAllSerializer
from pms_apps.activity_log.views import ActivityLogView
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.activity_log.serializer.response.get_all_user import ActivityLogUserResponseGetAllSerilizer
from pms_apps.activity_log.serializer.response.get_all_admin import ActivityLogAdminResponseGetAllSerilizer



class ActivityLogController:
    @extend_schema(
        description="Get all Logs for the user",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=ActivityLogUserResponseGetAllSerilizer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_for_user(request:Response) -> Response:
        return ActivityLogView().get_all_user(params=request.params)
    
    @extend_schema(
        description="Get all Logs for the admin",
        request=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=ActivityLogAdminResponseGetAllSerilizer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_for_admin(request:Response) -> Response:
        return ActivityLogView().get_all_admin(params=request.params)