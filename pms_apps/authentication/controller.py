from django.views.decorators.csrf import csrf_exempt

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication

from pms_apps.authentication.serializers_auth import (
    UserAuthSerializer,
    OTPVerifySerializer,
    UserAuthResponseSerializer,
    UserLoginSerializer,
)
from pms_apps.authentication.views import UserAuthView
from pms_apps.common.swagger import SwaggerPage

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
    
class AuthController:
    @extend_schema(
        description="Register a new user and send OTP.",
        request=UserAuthSerializer,
        responses=SwaggerPage.response(description="OTP sent successfully."),
        tags=["Authentication"],
    )
    @csrf_exempt
    @api_view(["POST"])
    @permission_classes([AllowAny])
    def register(request: Request) -> Response:
        return UserAuthView().register(params=request.data)

    @extend_schema(
        description="Login existing user and send OTP.",
        request=UserAuthSerializer,
        responses=SwaggerPage.response(description="OTP sent successfully."),
        tags=["Authentication"],
    )
    @csrf_exempt
    @api_view(["POST"])
    @permission_classes([AllowAny])
    def login(request: Request) -> Response:
        return UserAuthView().login(params=request.data)

    @extend_schema(
        description="Login with username and password, return JWT token.",
        request=UserLoginSerializer,
        responses=SwaggerPage.response(response=UserAuthResponseSerializer),
        tags=["Authentication"],
    )
    @csrf_exempt
    @api_view(["POST"])
    @permission_classes([AllowAny])
    def login_with_username(request: Request) -> Response:
        return UserAuthView().login_with_username(params=request.data)

    @extend_schema(
        description="Verify OTP and return JWT token.",
        request=OTPVerifySerializer,
        responses=SwaggerPage.response(response=UserAuthResponseSerializer),
        tags=["Authentication"],
    )
    @csrf_exempt
    @api_view(["POST"])
    @permission_classes([AllowAny])
    def verify_otp(request: Request) -> Response:
        return UserAuthView().verify_otp(params=request.data)
