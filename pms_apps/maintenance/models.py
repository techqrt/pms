from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


# ----------------------------
# Maintenance Manager
# ----------------------------
class MaintenanceManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="maintenance_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)  # e.g. HVAC, Electrical, Plumbing
    team_size = models.IntegerField(default=0)
    years_experience = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "maintenance_manager"

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
        specialization: str = "",
        team_size: int = 0,
        years_experience: int = 0,
    ) -> int:
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.specialization = specialization
        self.team_size = team_size
        self.years_experience = years_experience
        self.created_date_time = timezone.now()
        self.save()
        return self.manager_id_id

    @staticmethod
    def update(manager_id: int, name: str, dob=None, specialization: str = "", team_size: int = 0, years_experience: int = 0) -> int:
        m = MaintenanceManager.objects.get(manager_id=manager_id)
        m.name = name
        m.dob = dob
        m.specialization = specialization
        m.team_size = team_size
        m.years_experience = years_experience
        m.save()
        return m.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        MaintenanceManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        return MaintenanceManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "specialization", "team_size", "years_experience", "created_date_time",
            "manager_id__phone_number", "manager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            MaintenanceManager.objects.filter(filters).values(
                "manager_id", "name", "dob", "specialization", "team_size", "years_experience", "created_date_time",
                "manager_id__phone_number", "manager_id__email"
            )
        )


# ----------------------------
# Maintenance Employee
# ----------------------------
class MaintenanceEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="maintenance_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    assigned_tasks = models.IntegerField(default=0)
    manager_ref = models.ForeignKey(MaintenanceManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "maintenance_employee"

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
        specialization: str = "",
        assigned_tasks: int = 0,
        manager_ref: int = None,
    ) -> int:
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.designation = designation
        self.specialization = specialization
        self.assigned_tasks = assigned_tasks
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
        specialization: str = "",
        assigned_tasks: int = 0,
        manager_ref: int = None,
    ) -> int:
        e = MaintenanceEmployee.objects.get(employee_id=employee_id)
        e.name = name
        e.dob = dob
        e.designation = designation
        e.specialization = specialization
        e.assigned_tasks = assigned_tasks
        if manager_ref is not None:
            e.manager_ref_id = manager_ref
        e.save()
        return e.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        MaintenanceEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        return MaintenanceEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "designation", "specialization", "assigned_tasks", "manager_ref_id",
            "created_date_time", "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            MaintenanceEmployee.objects.filter(filters).values(
                "employee_id", "name", "dob", "designation", "specialization", "assigned_tasks", "manager_ref_id",
                "created_date_time", "employee_id__phone_number", "employee_id__email"
            )
        )


# ----------------------------
# Technician
# ----------------------------
class Technician(models.Model):
    technician_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="technician_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    skill_type = models.CharField(max_length=100, blank=True, null=True)  # e.g. Electrician, Plumber, Carpenter
    experience_years = models.IntegerField(default=0)
    assigned_jobs = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "technician"

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
        skill_type: str = "",
        experience_years: int = 0,
        assigned_jobs: int = 0,
    ) -> int:
        self.technician_id_id = technician_id
        self.name = name
        self.dob = dob
        self.skill_type = skill_type
        self.experience_years = experience_years
        self.assigned_jobs = assigned_jobs
        self.created_date_time = timezone.now()
        self.save()
        return self.technician_id_id

    @staticmethod
    def update(
        technician_id: int,
        name: str,
        dob=None,
        skill_type: str = "",
        experience_years: int = 0,
        assigned_jobs: int = 0,
    ) -> int:
        t = Technician.objects.get(technician_id=technician_id)
        t.name = name
        t.dob = dob
        t.skill_type = skill_type
        t.experience_years = experience_years
        t.assigned_jobs = assigned_jobs
        t.save()
        return t.technician_id_id

    @staticmethod
    def remove(technician_id: int) -> None:
        Technician.objects.get(technician_id=technician_id).delete()

    @staticmethod
    def get(technician_id: int) -> dict:
        return Technician.objects.filter(technician_id=technician_id).values(
            "technician_id", "name", "dob", "skill_type", "experience_years", "assigned_jobs", "created_date_time",
            "technician_id__phone_number", "technician_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            Technician.objects.filter(filters).values(
                "technician_id", "name", "dob", "skill_type", "experience_years", "assigned_jobs", "created_date_time",
                "technician_id__phone_number", "technician_id__email"
            )
        )
