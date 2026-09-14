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
from pms_apps.lead.models.lead import Lead
from pms_apps.marketing.models.marketing_employee import MarketingEmployee
from pms_apps.marketing.models.marketing_manager import MarketingManager
from pms_apps.property.models.property_employee import PropertyEmployee
from pms_apps.property.models.property_manager import PropertyManager
from pms_apps.maintenance.models.maintenance_employee import MaintenanceEmployee
from pms_apps.maintenance.models.maintenance_manager import MaintenanceManager
from pms_apps.maintenance.models.maintenance_technician import MaintenanceTechnician
from pms_apps.reception.models.reception_employee import ReceptionEmployee
from pms_apps.reception.models.reception_manager import ReceptionManager
from pms_apps.finance.models.finance_employee import FinanceEmployee
from pms_apps.finance.models.finance_manager import FinanceManager
from pms_apps.collection.models.collection_employee import CollectionEmployee
from pms_apps.collection.models.collection_manager import CollectionManager
from pms_apps.legal.models.legal_employee import LegalEmployee
from pms_apps.legal.models.legal_manager import LegalManager
from pms_apps.IT.models.IT_employee import ITEmployee
from pms_apps.IT.models.IT_manager import ITManager
from pms_apps.IT.models.IT_technician import ITTechnician
from pms_apps.hr.models import HREmployee
from pms_apps.checkin_checkout.models.check_in_check_out_employee import CheckInCheckOutEmployee
from pms_apps.checkin_checkout.models.check_in_check_out_manager import CheckInCheckOutManager

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

    # ----------------------------
    # LOGIN WITH USERNAME AND PASSWORD
    # ----------------------------
    def login_with_username(self, params):
        from pms_apps.authentication.serializers_auth import UserLoginSerializer
        from django.contrib.auth.hashers import make_password
        
        serializer = UserLoginSerializer(data=params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        try:
            # Try to find user by email or phone number
            user = User.objects.get(email=username) if "@" in username else User.objects.get(phone_number=username)

            # Check password - try Django's built-in hashing first
            password_matches = user.check_password(password)
            
            # Fallback: if password is stored as plain text (for backwards compatibility)
            if not password_matches and user.password == password:
                password_matches = True
                # Auto-hash the password for security
                user.set_password(password)
                user.save()
            
            if not password_matches:
                return Response(
                    {"error": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Generate token
            token = generate_jwt_token(user)

            # Save token in db
            user.access_token = token
            user.save()

            response_data = UserAuthResponseSerializer(user).data
            response_data["token"] = token

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
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

        #saving the token in db
        user.access_token = token
        user.save()

        response_data = UserAuthResponseSerializer(user).data
        response_data["token"] = token

        return Response(response_data, status=status.HTTP_200_OK)

    # ----------------------------------------------------
    # GET /auth/me/ - generic, role-agnostic "who am I" profile
    # ----------------------------------------------------
    def me_extract(self, user_id: int):
        """Returns the caller's own basic User fields plus their
        department-specific profile, reusing each department's existing
        Manager/Employee/Technician .get() method. Lives under /auth/,
        which is exempt from JWTAuthentication's department-permission gate
        entirely, so - unlike e.g. /marketing/manager/get/ - it can never
        403 a user just for belonging to a different department."""
        user_row = User.get(user_id=user_id)
        if user_row is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "User not found."},
            )

        department = user_row.get('department')
        role = user_row.get('role')

        profile_map = {
            ("Tenant", None): lambda: Lead.get(lead_id=user_id, include_profile_image=True),
            ("Landlord", None): lambda: Lead.get(lead_id=user_id, include_profile_image=True),
            ("Marketing", "Manager"): lambda: MarketingManager.get(manager_id=user_id),
            ("Marketing", "Employee"): lambda: MarketingEmployee.get(employee_id=user_id),
            ("Property", "Manager"): lambda: PropertyManager.get(manager_id=user_id),
            ("Property", "Employee"): lambda: PropertyEmployee.get(employee_id=user_id),
            ("Maintenance", "Manager"): lambda: MaintenanceManager.get(manager_id=user_id),
            ("Maintenance", "Employee"): lambda: MaintenanceEmployee.get(employee_id=user_id),
            ("Maintenance", "Technician"): lambda: MaintenanceTechnician.get(technician_id=user_id),
            ("Reception", "Manager"): lambda: ReceptionManager.get(manager_id=user_id),
            ("Reception", "Employee"): lambda: ReceptionEmployee.get(employee_id=user_id),
            ("Finance", "Manager"): lambda: FinanceManager.get(manager_id=user_id),
            ("Finance", "Employee"): lambda: FinanceEmployee.get(employee_id=user_id),
            ("Collection", "Manager"): lambda: CollectionManager.get(manager_id=user_id),
            ("Collection", "Employee"): lambda: CollectionEmployee.get(employee_id=user_id),
            ("Legal", "Manager"): lambda: LegalManager.get(manager_id=user_id),
            ("Legal", "Employee"): lambda: LegalEmployee.get(employee_id=user_id),
            ("IT", "Manager"): lambda: ITManager.get(manager_id=user_id),
            ("IT", "Employee"): lambda: ITEmployee.get(employee_id=user_id),
            ("IT", "Technician"): lambda: ITTechnician.get(technician_id=user_id),
            ("Check-In Check-Out", "Manager"): lambda: CheckInCheckOutManager.get(manager_id=user_id),
            ("Check-In Check-Out", "Employee"): lambda: CheckInCheckOutEmployee.get(employee_id=user_id),
            ("Owner", "Owner"): lambda: Owner.get(owner_id=user_id),
            ("General Manager", "General Manager"): lambda: GeneralManager.get(general_manager_id=user_id),
        }

        profile_fn = profile_map.get((department, role))
        profile = profile_fn() if profile_fn else None

        return Response(
            status=status.HTTP_200_OK,
            data={
                "userId": user_id,
                "name": user_row.get('name'),
                "phoneNumber": user_row.get('phone_number'),
                "email": user_row.get('email'),
                "department": department,
                "role": role,
                "profile": profile or {},
            },
        )

    # ----------------------------------------------------
    # Module Instance Creation Logic (unchanged)
    # ----------------------------------------------------
    def _create_module_instance(self, user, role, module):
        """Creates the appropriate module model instance dynamically."""
        from pms_apps.common.models.permissions import LeadPermission, PropertyPermission

        def new_lead_permission_id():
            # Every Manager/Employee gets their OWN permission record (never
            # shared) so it can be edited independently later. Defaults to
            # granted - a null record here previously meant the auth layer
            # silently denied cross-department access the role legitimately
            # needs (e.g. Check-In Check-Out staff reading Lead records),
            # with no way to grant it after the fact for departments that
            # have no update endpoint.
            return LeadPermission.objects.create(lead=True).permission_id

        def new_property_permission_id():
            return PropertyPermission.objects.create(property=True).permission_id

        # Global roles
        if role == "Owner":
            Owner.objects.create(owner_id=user)
            return
        elif role == "General Manager":
            GeneralManager.objects.create(general_manager_id=user)
            return

        # Module-based role mapping
        module_map = {
            "Tenant": lambda: Lead.objects.create(lead_id=user, purpose='Tenant', property_permissions_id=new_property_permission_id()),
            "Landlord": lambda: Lead.objects.create(lead_id=user, purpose='Landlord', property_permissions_id=new_property_permission_id()),
            "HR": lambda: HREmployee.objects.create(hr_employee_id=user),

            "Marketing": lambda: (
                MarketingManager.objects.create(manager_id=user, lead_permission_id=new_lead_permission_id(), property_permission_id=new_property_permission_id())
                if role == "Manager"
                else MarketingEmployee.objects.create(employee_id=user, lead_permission_id=new_lead_permission_id(), property_permission_id=new_property_permission_id())
            ),
            "Property": lambda: (
                PropertyManager.objects.create(manager_id=user)
                if role == "Manager"
                else PropertyEmployee.objects.create(employee_id=user)
            ),
            # Maintenance's Manager/Employee/Technician models only have a
            # property_permission field (no lead_permission at all).
            "Maintenance": lambda: (
                MaintenanceManager.objects.create(manager_id=user, property_permission_id=new_property_permission_id())
                if role == "Manager"
                else MaintenanceEmployee.objects.create(employee_id=user, property_permission_id=new_property_permission_id())
                if role == "Employee"
                else MaintenanceTechnician.objects.create(technician_id=user, property_permission_id=new_property_permission_id())
                if role == "Technician"
                else None
            ),
            # Reception/Finance/Collection/Legal/IT's Manager/Employee models
            # have neither lead_permission nor property_permission fields at
            # all - nothing to grant here.
            "Reception": lambda: (
                ReceptionManager.objects.create(manager_id=user)
                if role == "Manager"
                else ReceptionEmployee.objects.create(employee_id=user)
            ),
            "Finance": lambda: (
                FinanceManager.objects.create(manager_id=user)
                if role == "Manager"
                else FinanceEmployee.objects.create(employee_id=user)
            ),
            "Collection": lambda: (
                CollectionManager.objects.create(manager_id=user)
                if role == "Manager"
                else CollectionEmployee.objects.create(employee_id=user)
            ),
            "Legal": lambda: (
                LegalManager.objects.create(manager_id=user)
                if role == "Manager"
                else LegalEmployee.objects.create(employee_id=user)
            ),
            # IT's Manager/Employee/Technician models have neither
            # lead_permission nor property_permission fields at all.
            "IT": lambda: (
                ITManager.objects.create(manager_id=user)
                if role == "Manager"
                else ITEmployee.objects.create(employee_id=user)
                if role == "Employee"
                else ITTechnician.objects.create(technician_id=user)
                if role == "Technician"
                else None
            ),
            "Check-In Check-Out": lambda: (
                CheckInCheckOutManager.objects.create(manager_id=user, lead_permission_id=new_lead_permission_id(), property_permission_id=new_property_permission_id())
                if role == "Manager"
                else CheckInCheckOutEmployee.objects.create(employee_id=user, lead_permission_id=new_lead_permission_id(), property_permission_id=new_property_permission_id())
            ),
        }

        create_fn = module_map.get(module)
        if create_fn:
            create_fn()
        else:
            print(f"No model mapping found for module: {module}")
