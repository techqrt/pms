from django.db import models
from django.db.models import Q
from pms_apps.common.models import Country
from pms_apps.authentication.models import User
from pms_apps.lead.models.property_permission import PropertyPermission
#Lead.py
#LeadPermission.py - id fireig 

#FIX PROPERTY PERMISSION SPELLING
class Lead(models.Model):
    

    LEAD_TYPES = [
        ("Web User", "Web User"),
        ("Admin", "Admin"),
        ("Application", "Application"),
        ("WA", "WA"),
        ("Marketing Team", "Marketing Team"),
        ]

    PURPOSE_CHOICES = [
        ("Tenant", "Tenant"),
        ("Landlord", "Landlord"),
        ]

    lead_id = models.OneToOneField(
        to=User,
        verbose_name='Lead User',
        on_delete=models.DO_NOTHING,
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
        max_length=15,
    )
    
    last_name = models.CharField(
        verbose_name="Lastname",
        max_length=15
    )
    lead_origin = models.CharField(
        verbose_name="Lead Origin",
        choices=LEAD_TYPES,
        max_length=20
    )
    address = models.TextField(
        verbose_name="Address",
    )
    nationality = models.ForeignKey(
        verbose_name='Nationality',
        to=Country,
        on_delete=models.DO_NOTHING,
        null=True,
    )
    passport_or_id = models.CharField(
        verbose_name="Passport/ID",
        max_length=50,
    )
    purpose = models.CharField(
        verbose_name="Purpose",
        choices=PURPOSE_CHOICES,
        max_length=10,
    )
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
        default=True
    )

    class Meta:
        db_table = "lead"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.lead_origin})"

    def create(
        self,
        lead_id : int,
        lead_assign_to: int,
        first_name: str,
        last_name: str,
        lead_origin: str,
        address: str,
        nationality: int,
        passport_or_id: str,
        purpose: str,
        property_permissions_id : int
    ) -> int:
        self.lead_id_id = lead_id
        self.lead_assign_to_id = lead_assign_to
        self.first_name = first_name
        self.last_name = last_name
        self.lead_origin = lead_origin
        self.address = address
        self.nationality_id = nationality
        self.passport_or_id = passport_or_id
        self.purpose = purpose
        self.property_permissions = PropertyPermission(property_permissions_id)
        self.save()
        return self.lead_id

    @staticmethod
    def update(
        lead_id: int,
        lead_assign_to: int = None,
        first_name: str = None,
        last_name: str = None,
        lead_origin: str = None,
        address: str = None,
        nationality: int = None,
        passport_or_id: str = None,
        purpose: str = None,
        is_active: bool = None,
        property_permission_id : int = None,
    ) -> int:
        lead = Lead.objects.get(lead_id_id=lead_id)
        if lead_assign_to is not None:
            lead.lead_assign_to_id = lead_assign_to
        if first_name is not None:
            lead.first_name = first_name
        if last_name is not None:
            lead.last_name = last_name
        if lead_origin is not None:
            lead.lead_origin = lead_origin
        if address is not None:
            lead.address = address
        if nationality is not None:
            lead.nationality_id = nationality
        if passport_or_id is not None:
            lead.passport_or_id = passport_or_id
        if purpose is not None:
            lead.purpose = purpose
        if is_active is not None:
            lead.is_active = is_active
        if property_permission_id is not None: 
            lead.property_permissions = PropertyPermission(property_permission_id)

        lead.save()
        return lead.lead_id

    @staticmethod
    def remove(lead_id: int) -> None:
        lead = Lead.objects.get(lead_id=lead_id)
        lead.delete()
        return lead.lead_id

    @staticmethod
    def get(lead_id: int) -> dict:
        return Lead.objects.filter(lead_id__user_id=lead_id).values(
            "lead_id",  "first_name", "last_name", "lead_origin",
            "address", "nationality__name", "passport_or_id", "purpose",
            "created_at", "updated_at", "is_active","lead_assign_to__name","nationality__country_id",
            "lead_assign_to__user_id","lead_assign_to__phone_number", "lead_assign_to__email","property_permissions__permission_id","property_permissions__property"
        ).first()

    @staticmethod
    def get_all(
        sort_by : str = '',
        sort_order : str = '',
        filter_key : str = '',
        filter_value : str = '',
        search_key : str = '',
        ) -> list:
        data = Lead.objects.filter(is_active=True)
        if filter_key and filter_value:
            data = Lead.objects.filter(is_active=True,**{filter_key:filter_value})
        if search_key:
            data = Lead.objects.filter(
                Q(first_name__icontains = search_key) |
                Q(last_name__icontains = search_key) 
            )
        if sort_by:
            data = data.order_by(('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "lead_id", "lead_assign_to_id", "first_name", "last_name", "lead_origin",
                "address", "nationality", "passport_or_id", "purpose",
                "created_at", "updated_at", "is_active",
                "lead_assign_to__phone_number", "lead_assign_to__email","property_permissions__permission_id","property_permissions__property"
            )
            )
