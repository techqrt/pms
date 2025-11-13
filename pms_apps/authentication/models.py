from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
import random
from datetime import timedelta
from django.utils import timezone

from django.utils.timezone import now
from django.core.validators import RegexValidator


class User(AbstractBaseUser):
    DEPARTMENT_CHOICES = [
        ("Lead", "Lead"),
        ("Marketing Dept login", "Marketing Dept login"),
        ("Property Management login", "Property Management login"),
        ("Tenant Management Module", "Tenant Management Module"),
        ("Maintenance Dept login", "Maintenance Dept login"),
        ("Reception Dept login", "Reception Dept login"),
        ("Finance Dept Login", "Finance Dept Login"),
        ("Collection Dept login", "Collection Dept login"),
        ("Legal Dept Login", "Legal Dept Login"),
        ("IT Dept login", "IT Dept login"),
        ("IT Technician", "IT Technician"),
        ("Agreement Team", "Agreement Team"),   # Remove the department - Known as a Legal Dept
        ("General Manager", "General Manager"),
        ("Owner", "Owner"),
    ]

    ROLE_CHOICES = [
        ("Owner", "Owner"),
        ("General Manager", "General Manager"),
        ("Manager", "Manager"),
        ("Employee", "Employee"),
    ]

    user_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(blank=True, null=True)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)
    otp = models.IntegerField(null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.name or self.phone_number} ({self.department or 'No Dept'})"

    # Optional helper for OTP generation
    def generate_otp(self):
        import random
        otp = random.randint(100000, 999999)
        self.otp = otp
        self.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
        self.save()
        return otp
    
    def get(user_id : int) -> dict:
        return User.objects.filter(user_id=user_id).values(
            'user_id','phone_number','name','email','department','role').first()