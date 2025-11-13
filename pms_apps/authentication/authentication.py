import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from pms_apps.authentication.models import User  # Adjust this to your actual User model

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # No token provided, let other authentication classes handle it

        token = auth_header.split(" ")[1]  # Extract the token part
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        # Fetch the user (assuming `User` model has an `id` field)
        try:
            user = User.objects.get(user_id=payload["user_id"])
            user.role = payload.get("role")  # Attach role dynamically
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return user, None  # DRF expects a (user, auth) tuple

