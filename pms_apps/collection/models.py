from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


# ----------------------------
# Collection Manager
# ----------------------------
class CollectionManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="collection_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    total_collections = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    overdue_accounts_managed = models.IntegerField(default=0)
    team_size = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "collection_manager"

    def __str__(self):
        return f"{self.name} ({self.manager_id.phone_number})"

    # ----------------------
    # CRUD Operations
    # ----------------------

    def create(
        self,
        manager_id: int,
        name: str,
        dob=None,
        department: str = "",
        total_collections: float = 0.00,
        overdue_accounts_managed: int = 0,
        team_size: int = 0,
    ) -> int:
        """Create a new Collection Manager profile"""
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.total_collections = total_collections
        self.overdue_accounts_managed = overdue_accounts_managed
        self.team_size = team_size
        self.created_date_time = timezone.now()
        self.save()
        return self.manager_id_id

    @staticmethod
    def update(
        manager_id: int,
        name: str,
        dob=None,
        department: str = "",
        total_collections: float = 0.00,
        overdue_accounts_managed: int = 0,
        team_size: int = 0,
    ) -> int:
        """Update collection manager profile"""
        m = CollectionManager.objects.get(manager_id=manager_id)
        m.name = name
        m.dob = dob
        m.department = department
        m.total_collections = total_collections
        m.overdue_accounts_managed = overdue_accounts_managed
        m.team_size = team_size
        m.save()
        return m.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        """Delete collection manager profile"""
        CollectionManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        """Fetch single collection manager profile"""
        return CollectionManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "department", "total_collections",
            "overdue_accounts_managed", "team_size", "created_date_time",
            "manager_id__phone_number", "manager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all collection managers"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            CollectionManager.objects.filter(filters).values(
                "manager_id", "name", "dob", "department", "total_collections",
                "overdue_accounts_managed", "team_size", "created_date_time",
                "manager_id__phone_number", "manager_id__email"
            )
        )


# ----------------------------
# Collection Employee
# ----------------------------
class CollectionEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="collection_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True, null=True)   # e.g., Field Collector, Recovery Officer
    region = models.CharField(max_length=100, blank=True, null=True)
    collections_made = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    overdue_accounts_handled = models.IntegerField(default=0)
    manager_ref = models.ForeignKey(CollectionManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "collection_employee"

    def __str__(self):
        return f"{self.name} ({self.employee_id.phone_number})"

    # ----------------------
    # CRUD Operations
    # ----------------------

    def create(
        self,
        employee_id: int,
        name: str,
        dob=None,
        designation: str = "",
        region: str = "",
        collections_made: float = 0.00,
        overdue_accounts_handled: int = 0,
        manager_ref: int = None,
    ) -> int:
        """Create a new Collection Employee profile"""
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.designation = designation
        self.region = region
        self.collections_made = collections_made
        self.overdue_accounts_handled = overdue_accounts_handled
        if manager_ref:
            self.manager_ref_id = manager_ref
        self.created_date_time = timezone.now()
        self.save()
        return self.employee_id_id

    @staticmethod
    def update(
        employee_id: int,
        name: str,
        dob=None,
        designation: str = "",
        region: str = "",
        collections_made: float = 0.00,
        overdue_accounts_handled: int = 0,
        manager_ref: int = None,
    ) -> int:
        """Update collection employee profile"""
        e = CollectionEmployee.objects.get(employee_id=employee_id)
        e.name = name
        e.dob = dob
        e.designation = designation
        e.region = region
        e.collections_made = collections_made
        e.overdue_accounts_handled = overdue_accounts_handled
        if manager_ref is not None:
            e.manager_ref_id = manager_ref
        e.save()
        return e.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        """Delete collection employee"""
        CollectionEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        """Fetch single collection employee profile"""
        return CollectionEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "designation", "region", "collections_made",
            "overdue_accounts_handled", "manager_ref_id", "created_date_time",
            "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all collection employees"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            CollectionEmployee.objects.filter(filters).values(
                "employee_id", "name", "dob", "designation", "region", "collections_made",
                "overdue_accounts_handled", "manager_ref_id", "created_date_time",
                "employee_id__phone_number", "employee_id__email"
            )
        )
