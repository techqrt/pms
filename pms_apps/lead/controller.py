from drf_spectacular.utils import extend_schema
from pms_apps.common.swagger import SwaggerPage
from rest_framework.decorators import api_view
from pms_apps.common.serializer_validations import SerializerValidations
from .serilizers.request.create import LeadCreateRequestSerilizer
from .serilizers.request.update import LeadUpdateRequestSerilizer
from .serilizers.request.delete import LeadDeleteRequestSerilizer
from .serilizers.response.get import LeadResponseGetSerializer
from .serilizers.request.get import LeadGetRequestSerilizer
from .serilizers.response.get_all import LeadResponseGetAllSerilizer
from rest_framework.request import Request
from rest_framework.response import Response
from pms_apps.common.serializers.request.get_all import  GetAllSerializer
from .views import LeadView


class LeadViewController:

    @extend_schema(
        description="Add a Lead",
        request=LeadCreateRequestSerilizer,
        responses=SwaggerPage.response(description=LeadView().data_create)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=LeadCreateRequestSerilizer).validate
    def create(request:Request) -> Response:
        return LeadView().create_extract(params=request.params)
    
    @extend_schema(
        description="Update a Lead",
        request=LeadUpdateRequestSerilizer,
        responses=SwaggerPage.response(description=LeadView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=LeadUpdateRequestSerilizer).validate
    def update(request:Request) -> Response:
        return LeadView().update_extract(params=request.params)
    

    @extend_schema(
        description="Delete a Lead",
        parameters=LeadDeleteRequestSerilizer.get_parameters(),
        responses=SwaggerPage.response(description=LeadView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=LeadDeleteRequestSerilizer).validate
    def delete(request:Request) -> Response:
        return LeadView().delete_extract(params=request.params)
    

    @extend_schema(
        description="Get a Lead",
        parameters=LeadGetRequestSerilizer.get_parameters(),
        responses=SwaggerPage.response(response=LeadResponseGetSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=LeadGetRequestSerilizer).validate
    def get(request:Response) -> Response:
        return LeadView().get_extract(params=request.params)
    

    @extend_schema(
        description="Get all Lead",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=LeadResponseGetAllSerilizer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request:Response) -> Response:
        return LeadView().get_all_extract(params=request.params)