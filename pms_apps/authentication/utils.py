import jwt
import datetime
from django.conf import settings
from django.http import JsonResponse
from .models import User
from pms_apps.authentication.models import User

def send_otp_sms(phone_number, otp):
    """Send OTP via SMS using Twilio."""
    pass

def generate_jwt_token(user : User):
    """Generate JWT token for authenticated user."""
    payload = {
        'user_id': user.user_id,
        'role': user.role,
        'department': user.department,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'token': None,
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    payload['token'] = token
    
    return token


@staticmethod
def get_user_info_from_db(user_id: int) -> dict:
    return User.get(user_id=user_id)