from django.db import models


class CheckInUtilityReading(models.Model):
    UTILITY_TYPE_CHOICES = [
        ("Electricity", "Electricity"),
        ("Water", "Water"),
        ("Gas", "Gas"),
        ("Internet", "Internet"),
        ("AC Service", "AC Service"),
        ("Fuel", "Fuel"),
        ("Solar", "Solar"),
        ("Other Services", "Other Services"),
    ]

    STATUS_CHOICES = [
        ("Normal", "Normal"),
        ("Fixed", "Fixed"),
        ("Issues", "Issues"),
        ("Not Applicable", "Not Applicable"),
    ]

    check_in_utility_reading_id = models.AutoField(primary_key=True)
    check_in = models.ForeignKey(
        "checkin_checkout.CheckIn",
        on_delete=models.CASCADE,
        related_name="utility_readings"
    )
    utility_type = models.CharField(max_length=30, choices=UTILITY_TYPE_CHOICES)
    meter_no = models.CharField(max_length=50, null=True, blank=True)
    reading_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    consumption = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True)
    rate_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    charges = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Normal")
    remarks = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_in_utility_readings_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "check_in_utility_reading"
        ordering = ["-created_at"]
        verbose_name = "Check-In Utility Reading"
        verbose_name_plural = "Check-In Utility Readings"

    def __str__(self):
        return f"{self.utility_type} reading for CheckIn {self.check_in_id}"

    def create(
        self,
        check_in_id: int,
        utility_type: str,
        meter_no: str = None,
        reading_value=None,
        consumption=None,
        unit: str = None,
        rate_per_unit=None,
        charges=None,
        status: str = "Normal",
        remarks: str = "",
        created_by: int = None,
    ) -> int:
        self.check_in_id = check_in_id
        self.utility_type = utility_type
        self.meter_no = meter_no
        self.reading_value = reading_value
        self.consumption = consumption
        self.unit = unit
        self.rate_per_unit = rate_per_unit
        self.charges = charges
        self.status = status
        self.remarks = remarks
        self.created_by_id = created_by
        self.save()
        return self.check_in_utility_reading_id

    @staticmethod
    def get_all_for_check_in(check_in_id: int):
        return CheckInUtilityReading.objects.filter(
            check_in_id=check_in_id, is_active=True
        ).values(
            "check_in_utility_reading_id", "utility_type", "meter_no", "reading_value",
            "consumption", "unit", "rate_per_unit", "charges", "status", "remarks", "created_at",
        )

    @staticmethod
    def update(
        check_in_utility_reading_id: int,
        utility_type: str = None,
        meter_no: str = None,
        reading_value=None,
        consumption=None,
        unit: str = None,
        rate_per_unit=None,
        charges=None,
        status: str = None,
        remarks: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            reading = CheckInUtilityReading.objects.get(check_in_utility_reading_id=check_in_utility_reading_id)
        except CheckInUtilityReading.DoesNotExist:
            raise ValueError(f"Invalid Check-In Utility Reading Id: {check_in_utility_reading_id}")

        if utility_type is not None:
            reading.utility_type = utility_type
        if meter_no is not None:
            reading.meter_no = meter_no
        if reading_value is not None:
            reading.reading_value = reading_value
        if consumption is not None:
            reading.consumption = consumption
        if unit is not None:
            reading.unit = unit
        if rate_per_unit is not None:
            reading.rate_per_unit = rate_per_unit
        if charges is not None:
            reading.charges = charges
        if status is not None:
            reading.status = status
        if remarks is not None:
            reading.remarks = remarks

        reading.save()
        return reading.check_in_utility_reading_id

    @staticmethod
    def delete(check_in_utility_reading_id: int) -> None:
        CheckInUtilityReading.objects.filter(
            check_in_utility_reading_id=check_in_utility_reading_id
        ).update(is_active=False)
