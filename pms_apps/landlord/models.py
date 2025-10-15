from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


class Landlord(models.Model):
    landlord_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="landlord_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    owned_units = models.IntegerField(default=0)
    managed_properties = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "landlord"

    def __str__(self):
        return f"{self.name} ({self.landlord_id.phone_number})"

    # CRUD
    def create(self, landlord_id: int, name: str, dob=None, address: str = "", owned_units: int = 0, managed_properties: int = 0) -> int:
        self.landlord_id_id = landlord_id
        self.name = name
        self.dob = dob
        self.address = address
        self.owned_units = owned_units
        self.managed_properties = managed_properties
        self.created_date_time = timezone.now()
        self.save()
        return self.landlord_id_id

    @staticmethod
    def update(landlord_id: int, name: str, dob=None, address: str = "", owned_units: int = 0, managed_properties: int = 0) -> int:
        landlord = Landlord.objects.get(landlord_id=landlord_id)
        landlord.name = name
        landlord.dob = dob
        landlord.address = address
        landlord.owned_units = owned_units
        landlord.managed_properties = managed_properties
        landlord.save()
        return landlord.landlord_id_id

    @staticmethod
    def remove(landlord_id: int) -> None:
        Landlord.objects.get(landlord_id=landlord_id).delete()

    @staticmethod
    def get(landlord_id: int) -> dict:
        return Landlord.objects.filter(landlord_id=landlord_id).values(
            "landlord_id", "name", "dob", "address", "owned_units", "managed_properties", "created_date_time",
            "landlord_id__phone_number", "landlord_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            Landlord.objects.filter(filters).values(
                "landlord_id", "name", "dob", "address", "owned_units", "managed_properties", "created_date_time",
                "landlord_id__phone_number", "landlord_id__email"
            )
        )


class LandlordManager(models.Model):
    manager_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="landlord_manager_profile")
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    total_portfolio = models.IntegerField(default=0)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "landlord_manager"

    def __str__(self):
        return f"{self.name} ({self.manager_id.phone_number})"

    def create(self, manager_id: int, name: str, dob=None, total_portfolio: int = 0, specialization: str = "") -> int:
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.total_portfolio = total_portfolio
        self.specialization = specialization
        self.save()
        return self.manager_id_id

    @staticmethod
    def update(manager_id: int, name: str, dob=None, total_portfolio: int = 0, specialization: str = "") -> int:
        m = LandlordManager.objects.get(manager_id=manager_id)
        m.name = name
        m.dob = dob
        m.total_portfolio = total_portfolio
        m.specialization = specialization
        m.save()
        return m.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        LandlordManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        return LandlordManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "total_portfolio", "specialization", "created_date_time",
            "manager_id__phone_number", "manager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            LandlordManager.objects.filter(filters).values(
                "manager_id", "name", "dob", "total_portfolio", "specialization", "created_date_time",
                "manager_id__phone_number", "manager_id__email"
            )
        )


class LandlordEmployee(models.Model):
    employee_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="landlord_employee_profile")
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "landlord_employee"

    def __str__(self):
        return f"{self.name} ({self.employee_id.phone_number})"

    def create(self, employee_id: int, name: str, dob=None, designation: str = "", region: str = "") -> int:
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.designation = designation
        self.region = region
        self.created_date_time = timezone.now()
        self.save()
        return self.employee_id_id

    @staticmethod
    def update(employee_id: int, name: str, dob=None, designation: str = "", region: str = "") -> int:
        e = LandlordEmployee.objects.get(employee_id=employee_id)
        e.name = name
        e.dob = dob
        e.designation = designation
        e.region = region
        e.save()
        return e.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        LandlordEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        return LandlordEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "designation", "region", "created_date_time",
            "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            LandlordEmployee.objects.filter(filters).values(
                "employee_id", "name", "dob", "designation", "region", "created_date_time",
                "employee_id__phone_number", "employee_id__email"
            )
        )
