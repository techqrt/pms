from django.db import models
from django.db.models import Q
from pms_apps.helper_apis.models.country import Country
from pms_apps.helper_apis.models.nationality import Nationality
from pms_apps.helper_apis.models.city import City
from pms_apps.authentication.models import User
from pms_apps.common.models.permissions import PropertyPermission
from pms_apps.common.sentinels import NOT_PROVIDED

class Lead(models.Model):
    

    LEAD_TYPES = [
        ("Open Sooq", "Open Sooq"),
        ("OLX", "OLX"),
        ("Employee Referral", "Employee Referral"),
        ("Reference", "Reference"),
        ("Website Inquiry", "Website Inquiry"),
        ("Social Media", "Social Media"),
        ("Walk-in Customer", "Walk-in Customer"),
        ("Phone Call Inquiry", "Phone Call Inquiry"),
        ("Office Visit", "Office Visit"),
        ("Online Property Portal", "Online Property Portal"),
        ("Printing- Banner, Flex, Hoardings", "Printing- Banner, Flex, Hoardings"),
    ]

    PURPOSE_CHOICES = [
        ("Tenant", "Tenant"),
        ("Landlord", "Landlord"),
        ]
    
    LEAD_CATEGORY_CHOICES = [
        ("Bachelor", "Bachelor"),
        ("Married", "Married")
    ]

    TENANT_TYPE_CHOICES = [
        ("Individual", "Individual"),
        ("Corporate", "Corporate"),
    ]

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    MARITAL_STATUS_CHOICES = [
        ("Single", "Single"),
        ("Married", "Married"),
        ("Divorced", "Divorced"),
        ("Widowed", "Widowed"),
    ]

    lead_id = models.OneToOneField(
        to=User,
        verbose_name='Lead User',
        on_delete=models.DO_NOTHING,
        primary_key=True,
    )

    lead_assign_to = models.ForeignKey(
        verbose_name='Lead Assigned',
        to=User,
        on_delete=models.DO_NOTHING,
        related_name='user_assign',
        null=True,
    )
    
    first_name = models.CharField(
        verbose_name="Firstname",
        max_length=100,
    )

    last_name = models.CharField(
        verbose_name="Lastname",
        max_length=100
    )
    lead_category = models.CharField(
        verbose_name='Lead Category',
        choices=LEAD_CATEGORY_CHOICES,
        max_length=15,
        null=True
    )
    feedback = models.TextField(
        verbose_name="Feedback",
        null=True
    )
    lead_origin = models.CharField(
        verbose_name="Lead Origin",
        choices=LEAD_TYPES,
        max_length=50, null=True,
        blank=True
    )
    address = models.TextField(
        verbose_name="Address",null=True,
        blank=True
    )
    country = models.ForeignKey(
        verbose_name='Country',
        to=Country,
        on_delete=models.DO_NOTHING,
        null=True
    )
    po_box = models.CharField(
        verbose_name="PO Box",
        max_length=20, null=True,
        blank=True
    )
    profile_image = models.ImageField(
        verbose_name="Profile Image",
        max_length=500,
        upload_to='lead_profiles',
        null=True,
        blank=True
    )
    city = models.ForeignKey(
        verbose_name='City',
        to=City,
        on_delete=models.DO_NOTHING,
        null=True
    )
    nationality = models.ForeignKey(
        verbose_name='Nationality',
        to=Nationality,
        on_delete=models.DO_NOTHING,
        null=True
    )
    po_box = models.CharField(
        verbose_name="PO Box",
        max_length=20,null=True,
        blank=True
    )
    profile_image = models.ImageField(
        verbose_name="Profile Image",
        max_length=500,
        upload_to='lead_profiles',
        null=True,
        blank=True
    )
    passport_or_id = models.CharField(
        verbose_name="Passport/ID",
        max_length=50,null=True,
        blank=True
    )
    civil_id = models.CharField(
        verbose_name="Civil ID",
        max_length=50,
        null=True,
        blank=True,
    )
    purpose = models.CharField(
        verbose_name="Purpose",
        choices=PURPOSE_CHOICES,
        max_length=10,
    )
    email = models.EmailField(null=True, blank=True)
    tenant_code = models.CharField(max_length=100, null=True, blank=True)
    tenant_type = models.CharField(max_length=20, choices=TENANT_TYPE_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    alternate_mobile_number = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=200, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=20, null=True, blank=True)
    profession = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    estimated_closing_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(
        verbose_name="Created At",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated At",
        auto_now=True
    )
    property_permissions = models.ForeignKey(
        to=PropertyPermission,
        on_delete=models.DO_NOTHING,
        null=True
    )
    is_active = models.BooleanField(
        verbose_name="Is Active",
        default=False
    )

    class Meta:
        db_table = "lead"

    def _str_(self):
        return f"{self.first_name} {self.last_name} ({self.lead_origin})"
    
    @staticmethod
    def get_permissions(user_id : int) -> dict:
        lead = Lead.objects.filter(lead_id = user_id).first()

        permissions = {}
        if lead and lead.property_permissions:
            permissions["property"] = lead.property_permissions.property
        print(permissions)
        return {
            "permissions" : permissions
        }
        

    def create(
        self,
        lead_id : int,
        lead_assign_to: int,
        first_name: str,
        last_name: str,
        lead_origin: str,
        address: str,
        country_id : int,
        city_id : int,
        nationality_id : int,
        passport_or_id: str,
        purpose: str,
        property_permissions_id : int,
        po_box: str = None,
        feedback: str = None,
        lead_category: str = None,
        civil_id: str = None,
        estimated_closing_date = None,
        profile_image = None
    ) -> int:
        self.lead_id_id = lead_id
        self.lead_assign_to_id = lead_assign_to
        self.first_name = first_name
        self.last_name = last_name
        self.lead_origin = lead_origin
        self.address = address
        self.city_id = city_id
        self.country_id = country_id
        self.nationality_id = nationality_id
        self.passport_or_id = passport_or_id
        self.civil_id = civil_id
        self.purpose = purpose
        self.po_box = po_box
        self.feedback = feedback
        self.lead_category = lead_category
        self.estimated_closing_date = estimated_closing_date
        self.property_permissions_id = property_permissions_id
        if profile_image is not None:
            self.profile_image = profile_image
        self.save()
        return self.lead_id

    @staticmethod
    def update(
        lead_id: int,
        lead_assign_to: int = NOT_PROVIDED,
        first_name: str = None,
        last_name: str = None,
        lead_origin: str = NOT_PROVIDED,
        address: str = NOT_PROVIDED,
        country_id: int = NOT_PROVIDED,
        city_id: int = NOT_PROVIDED,
        nationality_id : int = NOT_PROVIDED,
        passport_or_id: str = NOT_PROVIDED,
        purpose: str = None,
        po_box: str = NOT_PROVIDED,
        feedback: str = NOT_PROVIDED,
        lead_category: str = NOT_PROVIDED,
        civil_id: str = NOT_PROVIDED,
        is_active: bool = None,
        property_permission_id : int = None,
        profile_image = None,
        tenant_code: str = None,
        tenant_type: str = None,
        date_of_birth=None,
        gender: str = None,
        marital_status: str = None,
        email: str = NOT_PROVIDED,
        alternate_mobile_number: str = None,
        emergency_contact_name: str = None,
        emergency_contact_number: str = None,
        profession: str = None,
        company_name: str = None,
        estimated_closing_date = NOT_PROVIDED,
    ) -> int:
        lead = Lead.objects.get(lead_id=lead_id)
        if lead_assign_to is not NOT_PROVIDED:
            lead.lead_assign_to_id = lead_assign_to
        if first_name is not None:
            lead.first_name = first_name
        if last_name is not None:
            lead.last_name = last_name
        if lead_origin is not NOT_PROVIDED:
            lead.lead_origin = lead_origin
        if address is not NOT_PROVIDED:
            lead.address = address
        if country_id is not NOT_PROVIDED:
            lead.country_id = country_id
        if city_id is not NOT_PROVIDED:
            lead.city_id = city_id
        if nationality_id is not NOT_PROVIDED:
            lead.nationality_id = nationality_id
        if passport_or_id is not NOT_PROVIDED:
            lead.passport_or_id = passport_or_id
        if civil_id is not NOT_PROVIDED:
            lead.civil_id = civil_id
        if purpose is not None:
            lead.purpose = purpose
        if po_box is not NOT_PROVIDED:
            lead.po_box = po_box
        if feedback is not NOT_PROVIDED:
            lead.feedback = feedback
        if lead_category is not NOT_PROVIDED:
            lead.lead_category = lead_category
        if is_active is not None:
            lead.is_active = is_active
        if property_permission_id is not None:
            lead.property_permissions_id = property_permission_id
        if profile_image is not None:
            lead.profile_image = profile_image
        if email is not NOT_PROVIDED:
            lead.email = email
        if tenant_code is not None:
            lead.tenant_code = tenant_code
        if tenant_type is not None:
            lead.tenant_type = tenant_type
        if date_of_birth is not None:
            lead.date_of_birth = date_of_birth
        if gender is not None:
            lead.gender = gender
        if marital_status is not None:
            lead.marital_status = marital_status
        if alternate_mobile_number is not None:
            lead.alternate_mobile_number = alternate_mobile_number
        if emergency_contact_name is not None:
            lead.emergency_contact_name = emergency_contact_name
        if emergency_contact_number is not None:
            lead.emergency_contact_number = emergency_contact_number
        if profession is not None:
            lead.profession = profession
        if company_name is not None:
            lead.company_name = company_name
        if estimated_closing_date is not NOT_PROVIDED:
            lead.estimated_closing_date = estimated_closing_date
        lead.save()
        return lead.lead_id

    @staticmethod
    def remove(lead_id: int) -> None:
        lead = Lead.objects.get(lead_id_id=lead_id)
        lead.delete()
        return lead.lead_id

    @staticmethod
    @staticmethod
    def get(lead_id: int, include_profile_image: bool = False) -> dict:
        fields = [
            "lead_id", "first_name", "last_name", "lead_category", "lead_origin",
            "address", "po_box", "feedback", "country__name", "city__name", "nationality__name", "passport_or_id", "civil_id", "purpose",
            "created_at", "updated_at", "is_active", "lead_assign_to__name",
            "lead_assign_to__user_id", "lead_assign_to__phone_number", "lead_assign_to__email", "property_permissions__permission_id", "property_permissions__property", "lead_id__phone_number", "email",
            "tenant_code", "tenant_type", "date_of_birth", "gender", "marital_status",
            "alternate_mobile_number", "emergency_contact_name", "emergency_contact_number", "profession", "company_name", "estimated_closing_date",
        ]
        if include_profile_image:
            fields.append("profile_image")
        return Lead.objects.filter(lead_id=lead_id).values(*fields).first()

    @staticmethod
    def get_all(
        sort_by : str = '',
        sort_order : str = '',
        filter_key : str = '',
        filter_value : str = '',
        search_key : str = '',
        ) -> list:
        data = Lead.objects.all()
        if filter_key and filter_value:
            data = Lead.objects.filter(**{filter_key:filter_value})
        if search_key:
            data = Lead.objects.filter(
                Q(first_name__icontains = search_key) |
                Q(last_name__icontains = search_key) 
            )
        if sort_by:
            data = data.order_by(('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "lead_id", "lead_assign_to_id", "first_name", "last_name", "lead_category", "lead_origin",
                "address", "po_box", "feedback", "country__name", "city__name", "nationality__name", "passport_or_id", "civil_id", "purpose",
                "created_at", "updated_at", "is_active", "lead_assign_to__name",
                "lead_assign_to__phone_number", "lead_assign_to__email", "property_permissions__permission_id", "property_permissions__property", "lead_id__phone_number", "profile_image", "email",
                "tenant_code", "tenant_type", "date_of_birth", "gender", "marital_status",
                "alternate_mobile_number", "emergency_contact_name", "emergency_contact_number", "profession", "company_name", "estimated_closing_date",
            )
            )

    @staticmethod
    def get_all_by_assigned_user(
        manager_user_id : int,
        sort_by : str = '',
        sort_order : str = '',
        filter_key : str = '',
        filter_value : str = '',
        search_key : str = '',
        ) -> list:
        data = Lead.objects.filter(lead_assign_to__user_id=manager_user_id)
        if filter_key and filter_value:
            data = Lead.objects.filter(lead_assign_to__user_id=manager_user_id, **{filter_key:filter_value})
        if search_key:
            data = Lead.objects.filter(
                Q(first_name__icontains = search_key) |
                Q(last_name__icontains = search_key),
                lead_assign_to__user_id=manager_user_id
            )
        if sort_by:
            data = data.order_by(('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "lead_id", "lead_assign_to_id", "first_name", "last_name", "lead_category", "lead_origin",
                "address", "po_box", "feedback", "country__name", "city__name", "nationality__name", "passport_or_id", "civil_id", "purpose",
                "created_at", "updated_at", "is_active", "lead_assign_to__name",
                "lead_assign_to__phone_number", "lead_assign_to__email", "property_permissions__permission_id", "property_permissions__property", "lead_id__phone_number", "profile_image", "email",
                "tenant_code", "tenant_type", "date_of_birth", "gender", "marital_status",
                "alternate_mobile_number", "emergency_contact_name", "emergency_contact_number", "profession", "company_name", "estimated_closing_date",
            )
            )