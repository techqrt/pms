import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from pms.constants import Constants
from pms_apps.common.utils import Utils 
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from pms_apps.common.dataclasses.request.permission import Permissions,PermissionsMarketing,PermissionMaintenance,PermissionReception,PermissionFinance,PermissionCollection,PermissionLegal,PermissionIT,PermissionGeneralManager,PermissionHR,PermissionOwner, PermissionsProperty,PermissionsLead
from pms_apps.activity_log.middlewares.log_middleware import local
from pms_apps.authentication.models import User  # Adjust this to your actual User model
from pms_apps.authentication.utils import get_user_info_from_db

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None 

        token = auth_header.split(" ")[1]  # Extract the token part
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        user_info = get_user_info_from_db(user_id=payload["user_id"])

        
        if token != user_info['access_token']:
            raise AuthenticationFailed(Constants.invalid_access_token)

        try:
            user = User.objects.get(user_id=payload["user_id"])
            local.user_id = user.user_id
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")
        
        token_role = payload.get("role")
        token_department = payload.get("department")


        if token_role and token_role != user.role:
            raise AuthenticationFailed("Token role mismatch")

        if token_department and token_department != user.department:
            raise AuthenticationFailed("Token department mismatch")

        payload['permissions'] = user.get_permissions()

        if not self.validate_permissions(request=request, payload=payload):
                raise AuthenticationFailed(Constants.forbidden_access)
        
        permissions = map_permissions_from_payload(payload['permissions'])

        payload['permissions'] = permissions

        request.payload = payload

        return user, payload 
    
    def validate_permissions(self, request, payload) -> bool:

        path = request.path.lower().split('/')
        permissions = payload.get('permissions',{})

        depeartment = payload.get('department').lower()
        if depeartment == 'tenant' or depeartment == 'landlord':
            depeartment = 'lead'

        permissions_mapping = {
            'lead' : permissions.get('lead',False),
            'property': permissions.get('property',False),
            'marketing' : permissions.get('marketing',False),
            'maintenance' : permissions.get('maintenance',False),
            'reception' : permissions.get('reception',False),
            'finance' : permissions.get('finance',False),
            'collection' : permissions.get('collection',False),
            'legal' : permissions.get('legal',False),
            'it' : permissions.get('it',False),
            'general manager' : permissions.get('general manager',False),
            'hr' : permissions.get('hr',False),
            'owner' : permissions.get('owner',False),
        }
        permissions_mapping.pop(depeartment)

        for key, value in permissions_mapping.items():
            if key in path:
                    if not value: 
                        return False

        return True


def error_response(status_code=status.HTTP_401_UNAUTHORIZED, data=Constants.auth_error) -> Response:
    response_data = Utils.error_response_data(message=data, error=[data])
    response = Response(status=status_code, data=response_data)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response

def map_permissions_from_payload(payload_permissions):
    return Permissions(
        property=PermissionsProperty(
            property=payload_permissions.get('property', False),
        ),
        lead=PermissionsLead(
            lead=payload_permissions.get('lead', False),
        ),
        marketing=PermissionsMarketing(
            marketing=payload_permissions.get('marketing', False),
        ),
        maintenance=PermissionMaintenance(
            maintenance=payload_permissions.get('maintenance', False),
        ),
        reception=PermissionReception(
            reception=payload_permissions.get('reception', False),
        ),
        finance=PermissionFinance(
            finance=payload_permissions.get('finance', False),
        ),
        collection=PermissionCollection(
            collection=payload_permissions.get('collection', False),
        ),
        legal=PermissionLegal(
            legal=payload_permissions.get('legal', False),
        ),
        it=PermissionIT(
            it=payload_permissions.get('it', False),
        ),
        general_manager=PermissionGeneralManager(
            general_manager=payload_permissions.get('general_manager', False),
        ),
        hr=PermissionHR(
            hr=payload_permissions.get('hr', False),
        ),
        owner=PermissionOwner(
            owner=payload_permissions.get('owner', False),
        ),
    )

