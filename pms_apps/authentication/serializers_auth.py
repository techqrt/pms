from rest_framework import serializers
from pms_apps.authentication.models import User


class UserAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    role = serializers.ChoiceField(
        choices=[choice[0] for choice in User.ROLE_CHOICES],  # dynamically from model
        help_text="Role of the user."
    )
    module = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        phone_number = data.get("phone_number")
        role = data.get("role")
        module = data.get("module")

        if not phone_number:
            raise serializers.ValidationError({"phone_number": "Phone number is required."})
        if not role:
            raise serializers.ValidationError({"role": "Role is required."})
        if not module:
            raise serializers.ValidationError({"module": "Module is required."})

        return data


class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)

    def validate(self, data):
        otp = data.get("otp")

        if not otp:
            raise serializers.ValidationError({"otp": "OTP is required."})
        if not otp.isdigit():
            raise serializers.ValidationError({"otp": "OTP must contain only digits."})
        if len(otp) != 6:
            raise serializers.ValidationError({"otp": "OTP must be 6 digits long."})

        return data


class UserAuthResponseSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=False, help_text="JWT token (generated at runtime).")

    class Meta:
        model = User
        fields = (
            "user_id",
            "phone_number",
            "email",
            "role",
            "department",
            "token",
            "otp"
        )
        read_only_fields = ("user_id", "phone_number", "email", "role", "department","otp")
