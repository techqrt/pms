from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone

from pms_apps.authentication.models import User
from pms_apps.general_manager.models import GeneralManager
from pms_apps.owner.models import Owner
from pms_apps.authentication.serializers_auth import (
    UserAuthSerializer,
    OTPVerifySerializer,
    UserAuthResponseSerializer,
)
from pms_apps.authentication.utils import send_otp_sms, generate_jwt_token

# Import module models

from pms_apps.marketing.models import MarketingManager, MarketingEmployee
from pms_apps.property.models.property_employee import PropertyManager, PropertyEmployee
from pms_apps.maintenance.models import MaintenanceManager, MaintenanceEmployee, Technician
from pms_apps.reception.models import ReceptionManager, ReceptionEmployee
from pms_apps.finance.models import FinanceManager, FinanceEmployee
from pms_apps.collection.models import CollectionManager, CollectionEmployee
from pms_apps.legal.models import LegalManager, LegalEmployee
from pms_apps.IT.models import ITManager, ITEmployee, ITTechnician
from pms_apps.agreement_team.models import AgreementTeamManager, AgreementTeamEmployee


class UserAuthView(APIView):
    permission_classes = [AllowAny]

    # ----------------------------
    # REGISTER (for new users)
    # ----------------------------
    def register(self, params):
        serializer = UserAuthSerializer(data=params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data.get("phone_number")
        role = serializer.validated_data.get("role")
        module = serializer.validated_data.get("module")

        # Prevent duplicate registration
        if User.objects.filter(phone_number=phone_number).exists():
            return Response(
                {"error": "User already exists. Please login instead."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                # Create new user
                user = User.objects.create(
                    phone_number=phone_number,
                    role=role,
                    department=module,
                    created_date_time=timezone.now(),
                )

                # Create related module instance
                self._create_module_instance(user, role, module)

                # Generate OTP
                otp = user.generate_otp()
                send_otp_sms(phone_number, otp)

                return Response(
                    {"message": "Registration successful. OTP sent successfully."},
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ----------------------------
    # LOGIN (for existing users)
    # ----------------------------
    def login(self, params):
        serializer = UserAuthSerializer(data=params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data.get("phone_number")

        try:
            user = User.objects.get(phone_number=phone_number)

            # Generate OTP for login
            otp = user.generate_otp()
            send_otp_sms(phone_number, otp)

            return Response(
                {"message": "Login successful. OTP sent successfully."},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found. Please register first."},
                status=status.HTTP_404_NOT_FOUND,
            )

    # ----------------------------------------------------
    # OTP Verification (same as before)
    # ----------------------------------------------------
    def verify_otp(self, params):
        serializer = OTPVerifySerializer(data=params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        otp = serializer.validated_data.get("otp")

        try:
            user = User.objects.get(otp=otp, otp_expiry__gte=timezone.now())
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid or expired OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Reset OTP
        user.otp = None
        user.otp_expiry = None
        user.save()

        # Generate token
        token = generate_jwt_token(user)
        response_data = UserAuthResponseSerializer(user).data
        response_data["token"] = token

        return Response(response_data, status=status.HTTP_200_OK)

    # ----------------------------------------------------
    # Module Instance Creation Logic (unchanged)
    # ----------------------------------------------------
    def _create_module_instance(self, user, role, module):
        """Creates the appropriate module model instance dynamically."""

        # Global roles
        if role == "Owner":
            Owner.objects.create(owner_id=user)
            return
        elif role == "General Manager":
            GeneralManager.objects.create(generalmanager_id=user)
            return

        # Module-based role mapping
        module_map = {

            "Marketing Dept login": lambda: (
                MarketingManager.objects.create(manager_id=user)
                if role == "Manager"
                else MarketingEmployee.objects.create(employee_id=user)
            ),
            "Property Management login": lambda: (
                PropertyManager.objects.create(manager_id=user)
                if role == "Manager"
                else PropertyEmployee.objects.create(employee_id=user)
            ),
            "Maintenance Dept login": lambda: (
                MaintenanceManager.objects.create(manager_id=user)
                if role == "Manager"
                else MaintenanceEmployee.objects.create(employee_id=user)
            ),
            "Reception Dept login": lambda: (
                ReceptionManager.objects.create(manager_id=user)
                if role == "Manager"
                else ReceptionEmployee.objects.create(employee_id=user)
            ),
            "Finance Dept Login": lambda: (
                FinanceManager.objects.create(manager_id=user)
                if role == "Manager"
                else FinanceEmployee.objects.create(employee_id=user)
            ),
            "Collection Dept login": lambda: (
                CollectionManager.objects.create(manager_id=user)
                if role == "Manager"
                else CollectionEmployee.objects.create(employee_id=user)
            ),
            "Legal Dept Login": lambda: (
                LegalManager.objects.create(manager_id=user)
                if role == "Manager"
                else LegalEmployee.objects.create(employee_id=user)
            ),
            "IT Dept login": lambda: (
                ITManager.objects.create(manager_id=user)
                if role == "Manager"
                else ITEmployee.objects.create(employee_id=user)
            ),
            "IT Technician": lambda: ITTechnician.objects.create(technician_id=user),
            "Agreement Team": lambda: (
                AgreementTeamManager.objects.create(manager_id=user)
                if role == "Manager"
                else AgreementTeamEmployee.objects.create(employee_id=user)
            ),
        }

        create_fn = module_map.get(module)
        if create_fn:
            create_fn()
        else:
            print(f"No model mapping found for module: {module}")
