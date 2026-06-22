from rest_framework import serializers
from pms_apps.authentication.models import User


class UserAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    role = serializers.ChoiceField(
        choices=[choice[0] for choice in User.ROLE_CHOICES],
        required=False,
    )
    module = serializers.CharField(required=True)

    MODULE_TO_ROLE_MAPPINGS = {
        "Collection": ("Manager", "Employee"),
        "Finance": ("Manager", "Employee"),
        "General Manager": ("General Manager",),
        "HR": ("Employee",),
        "IT": ("Manager", "Employee", "Technician"),
        "Legal": ("Manager", "Employee"),
        "Maintenance": ("Manager", "Employee", "Technician"),
        "Marketing": ("Manager", "Employee"),
        "Owner": ("Owner",),
        "Property": ("Employee", "Manager"),
        "Reception": ("Manager", "Employee"),
        "Check-In Check-Out": ("Manager", "Employee"),
    }

    def validate(self, data):
        phone_number = data.get("phone_number")
        role = data.get("role")
        module = data.get("module")

        if not phone_number:
            raise serializers.ValidationError(
                {"phone_number": "Phone number is required."}
            )

        if module in ["Tenant", "Landlord"]:
            data.pop("role", None)
            return data

        if module not in self.MODULE_TO_ROLE_MAPPINGS:
            raise serializers.ValidationError(
                {"module": "Not a valid module"}
            )

        if not role:
            raise serializers.ValidationError(
                {"role": "Role is required for this module"}
            )

        if role not in self.MODULE_TO_ROLE_MAPPINGS[module]:
            raise serializers.ValidationError(
                {"role": "Not a valid role for this module"}
            )

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


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, help_text="Email or phone number")
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username:
            raise serializers.ValidationError(
                {"username": "Username (email or phone number) is required."}
            )
        if not password:
            raise serializers.ValidationError(
                {"password": "Password is required."}
            )

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
