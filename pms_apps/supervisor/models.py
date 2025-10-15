from django.db import models
from django.utils import timezone
from pms_apps.authentication.models import User


class Supervisor(models.Model):
    # Link directly with User (each user can have one Supervisor profile)
    supervisor_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="supervisor_profile")

    # Extra fields specific to Supervisor
    name = models.CharField(max_length=100, default='')
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)   # e.g., Operations, Maintenance, Sales
    team_size = models.IntegerField(default=0)
    shift = models.CharField(max_length=50, blank=True, null=True)         # e.g., Morning, Night, Rotational

    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "supervisor"

    def __str__(self):
        return f"{self.name} ({self.supervisor_id.username})"

    # ----------------------
    # Static CRUD Operations
    # ----------------------

    def create(self, supervisor_id: int, name: str, dob=None, department: str = "", team_size: int = 0, shift: str = "") -> int:
        """Create a new Supervisor profile"""
        self.supervisor_id_id = supervisor_id
        self.name = name
        self.dob = dob
        self.department = department
        self.team_size = team_size
        self.shift = shift
        self.created_date_time = timezone.now()
        self.save()
        return self.supervisor_id_id

    @staticmethod
    def update(supervisor_id: int, name: str, dob=None, department: str = "", team_size: int = 0, shift: str = "") -> int:
        """Update supervisor profile basic info"""
        supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)
        supervisor.name = name
        supervisor.dob = dob
        supervisor.department = department
        supervisor.team_size = team_size
        supervisor.shift = shift
        supervisor.save()
        return supervisor.supervisor_id_id

    @staticmethod
    def remove(supervisor_id: int) -> None:
        """Delete supervisor profile"""
        Supervisor.objects.get(supervisor_id=supervisor_id).delete()

    @staticmethod
    def get(supervisor_id: int) -> dict:
        """Fetch single supervisor profile details"""
        return Supervisor.objects.filter(supervisor_id=supervisor_id).values(
            "supervisor_id", "name", "dob", "department", "team_size", "shift", "created_date_time",
            "supervisor_id__username", "supervisor_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all supervisor profiles (with optional search by name)"""
        from django.db.models import Q
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)

        return list(
            Supervisor.objects.filter(filters).values(
                "supervisor_id", "name", "dob", "department", "team_size", "shift", "created_date_time",
                "supervisor_id__username", "supervisor_id__email"
            )
        )
