from django.db import models
from pms_apps.authentication.models import User

# Create your models here.
class HREmployee(models.Model):
    hr_employee_id = models.OneToOneField(
        to=User,
        on_delete=models.DO_NOTHING
    )
    name = models.CharField()