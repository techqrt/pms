from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


# ----------------------------
# IT Manager
# ----------------------------
class ITManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="it_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    projects_managed = models.IntegerField(default=0)
    systems_overseen = models.IntegerField(default=0)
    team_size = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "it_manager"

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
        projects_managed: int = 0,
        systems_overseen: int = 0,
        team_size: int = 0,
    ) -> int:
        """Create a new IT Manager profile"""
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.projects_managed = projects_managed
        self.systems_overseen = systems_overseen
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
        projects_managed: int = 0,
        systems_overseen: int = 0,
        team_size: int = 0,
    ) -> int:
        """Update IT manager profile"""
        m = ITManager.objects.get(manager_id=manager_id)
        m.name = name
        m.dob = dob
        m.department = department
        m.projects_managed = projects_managed
        m.systems_overseen = systems_overseen
        m.team_size = team_size
        m.save()
        return m.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        """Delete IT manager profile"""
        ITManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        """Fetch single IT manager"""
        return ITManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "department",
            "projects_managed", "systems_overseen", "team_size",
            "created_date_time", "manager_id__phone_number", "manager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all IT managers"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            ITManager.objects.filter(filters).values(
                "manager_id", "name", "dob", "department",
                "projects_managed", "systems_overseen", "team_size",
                "created_date_time", "manager_id__phone_number", "manager_id__email"
            )
        )


# ----------------------------
# IT Employee
# ----------------------------
class ITEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="it_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    role_title = models.CharField(max_length=100, blank=True, null=True)  # e.g., Developer, SysAdmin
    tickets_resolved = models.IntegerField(default=0)
    projects_assigned = models.IntegerField(default=0)
    specialization = models.CharField(max_length=100, blank=True, null=True)  # e.g., Backend, Networking
    manager_ref = models.ForeignKey(ITManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "it_employee"

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
        role_title: str = "",
        tickets_resolved: int = 0,
        projects_assigned: int = 0,
        specialization: str = "",
        manager_ref: int = None,
    ) -> int:
        """Create a new IT Employee profile"""
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.role_title = role_title
        self.tickets_resolved = tickets_resolved
        self.projects_assigned = projects_assigned
        self.specialization = specialization
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
        role_title: str = "",
        tickets_resolved: int = 0,
        projects_assigned: int = 0,
        specialization: str = "",
        manager_ref: int = None,
    ) -> int:
        """Update IT employee profile"""
        e = ITEmployee.objects.get(employee_id=employee_id)
        e.name = name
        e.dob = dob
        e.role_title = role_title
        e.tickets_resolved = tickets_resolved
        e.projects_assigned = projects_assigned
        e.specialization = specialization
        if manager_ref is not None:
            e.manager_ref_id = manager_ref
        e.save()
        return e.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        """Delete IT employee profile"""
        ITEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        """Fetch single IT employee"""
        return ITEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "role_title",
            "tickets_resolved", "projects_assigned", "specialization",
            "manager_ref_id", "created_date_time",
            "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all IT employees"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            ITEmployee.objects.filter(filters).values(
                "employee_id", "name", "dob", "role_title",
                "tickets_resolved", "projects_assigned", "specialization",
                "manager_ref_id", "created_date_time",
                "employee_id__phone_number", "employee_id__email"
            )
        )


# ----------------------------
# IT Technician
# ----------------------------
class ITTechnician(models.Model):
    technician_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="it_technician_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    skill_area = models.CharField(max_length=100, blank=True, null=True)  # e.g., Hardware, Network Support
    tickets_closed = models.IntegerField(default=0)
    experience_years = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "it_technician"

    def __str__(self):
        return f"{self.name} ({self.technician_id.phone_number})"

    # ----------------------
    # CRUD Operations
    # ----------------------

    def create(
        self,
        technician_id: int,
        name: str,
        dob=None,
        skill_area: str = "",
        tickets_closed: int = 0,
        experience_years: int = 0,
    ) -> int:
        """Create a new IT Technician profile"""
        self.technician_id_id = technician_id
        self.name = name
        self.dob = dob
        self.skill_area = skill_area
        self.tickets_closed = tickets_closed
        self.experience_years = experience_years
        self.created_date_time = timezone.now()
        self.save()
        return self.technician_id_id

    @staticmethod
    def update(
        technician_id: int,
        name: str,
        dob=None,
        skill_area: str = "",
        tickets_closed: int = 0,
        experience_years: int = 0,
    ) -> int:
        """Update IT Technician profile"""
        t = ITTechnician.objects.get(technician_id=technician_id)
        t.name = name
        t.dob = dob
        t.skill_area = skill_area
        t.tickets_closed = tickets_closed
        t.experience_years = experience_years
        t.save()
        return t.technician_id_id

    @staticmethod
    def remove(technician_id: int) -> None:
        """Delete IT Technician profile"""
        ITTechnician.objects.get(technician_id=technician_id).delete()

    @staticmethod
    def get(technician_id: int) -> dict:
        """Fetch single IT Technician"""
        return ITTechnician.objects.filter(technician_id=technician_id).values(
            "technician_id", "name", "dob", "skill_area",
            "tickets_closed", "experience_years", "created_date_time",
            "technician_id__phone_number", "technician_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all IT Technicians"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            ITTechnician.objects.filter(filters).values(
                "technician_id", "name", "dob", "skill_area",
                "tickets_closed", "experience_years", "created_date_time",
                "technician_id__phone_number", "technician_id__email"
            )
        )
