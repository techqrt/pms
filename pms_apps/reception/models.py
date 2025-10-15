from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


# ----------------------------
# Reception Manager
# ----------------------------
class ReceptionManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="reception_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    team_size = models.IntegerField(default=0)
    front_desk_count = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "reception_manager"

    def __str__(self):
        return f"{self.name} ({self.manager_id.phone_number})"

    # ----------------------
    # CRUD Operations
    # ----------------------

    def create(self, manager_id: int, name: str, dob=None, department: str = "", team_size: int = 0, front_desk_count: int = 0) -> int:
        """Create a new Reception Manager profile"""
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.team_size = team_size
        self.front_desk_count = front_desk_count
        self.created_date_time = timezone.now()
        self.save()
        return self.manager_id_id

    @staticmethod
    def update(manager_id: int, name: str, dob=None, department: str = "", team_size: int = 0, front_desk_count: int = 0) -> int:
        """Update reception manager profile"""
        m = ReceptionManager.objects.get(manager_id=manager_id)
        m.name = name
        m.dob = dob
        m.department = department
        m.team_size = team_size
        m.front_desk_count = front_desk_count
        m.save()
        return m.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        """Delete reception manager profile"""
        ReceptionManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        """Fetch single reception manager profile"""
        return ReceptionManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "department", "team_size", "front_desk_count",
            "created_date_time", "manager_id__phone_number", "manager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all reception managers"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            ReceptionManager.objects.filter(filters).values(
                "manager_id", "name", "dob", "department", "team_size", "front_desk_count",
                "created_date_time", "manager_id__phone_number", "manager_id__email"
            )
        )


# ----------------------------
# Reception Employee
# ----------------------------
class ReceptionEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="reception_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    shift = models.CharField(max_length=100, blank=True, null=True)            # e.g. Morning, Evening
    desk_number = models.CharField(max_length=50, blank=True, null=True)
    calls_handled = models.IntegerField(default=0)
    visitors_logged = models.IntegerField(default=0)
    manager_ref = models.ForeignKey(ReceptionManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "reception_employee"

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
        shift: str = "",
        desk_number: str = "",
        calls_handled: int = 0,
        visitors_logged: int = 0,
        manager_ref: int = None,
    ) -> int:
        """Create a new Reception Employee profile"""
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.shift = shift
        self.desk_number = desk_number
        self.calls_handled = calls_handled
        self.visitors_logged = visitors_logged
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
        shift: str = "",
        desk_number: str = "",
        calls_handled: int = 0,
        visitors_logged: int = 0,
        manager_ref: int = None,
    ) -> int:
        """Update reception employee profile"""
        e = ReceptionEmployee.objects.get(employee_id=employee_id)
        e.name = name
        e.dob = dob
        e.shift = shift
        e.desk_number = desk_number
        e.calls_handled = calls_handled
        e.visitors_logged = visitors_logged
        if manager_ref is not None:
            e.manager_ref_id = manager_ref
        e.save()
        return e.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        """Delete reception employee profile"""
        ReceptionEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        """Fetch single reception employee profile"""
        return ReceptionEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "shift", "desk_number",
            "calls_handled", "visitors_logged", "manager_ref_id",
            "created_date_time", "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all reception employees"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            ReceptionEmployee.objects.filter(filters).values(
                "employee_id", "name", "dob", "shift", "desk_number",
                "calls_handled", "visitors_logged", "manager_ref_id",
                "created_date_time", "employee_id__phone_number", "employee_id__email"
            )
        )
