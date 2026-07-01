from django.db import models


class CheckOutInspectionItem(models.Model):
    CATEGORY_CHOICES = [
        ("Walls & Ceilings", "Walls & Ceilings"),
        ("Door & Windows", "Door & Windows"),
        ("Electrical Fittings", "Electrical Fittings"),
        ("Plumbing", "Plumbing"),
        ("Kitchen", "Kitchen"),
        ("Bathrooms", "Bathrooms"),
        ("Furniture & Fixtures", "Furniture & Fixtures"),
        ("Hall", "Hall"),
        ("Others", "Others"),
    ]

    INSPECTION_STATUS_CHOICES = [
        ("Good", "Good"),
        ("Issue", "Issue"),
        ("Not Applicable", "Not Applicable"),
    ]

    SEVERITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    REPAIR_STATUS_CHOICES = [
        ("Required", "Required"),
        ("Pending", "Pending"),
        ("Repaired", "Repaired"),
    ]

    ITEM_APPROVAL_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
    ]

    check_out_inspection_item_id = models.AutoField(primary_key=True)
    check_out = models.ForeignKey(
        "checkin_checkout.CheckOut",
        on_delete=models.CASCADE,
        related_name="inspection_items"
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    item_name = models.CharField(max_length=255)
    inspection_status = models.CharField(max_length=20, choices=INSPECTION_STATUS_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, null=True, blank=True)
    repair_status = models.CharField(max_length=20, choices=REPAIR_STATUS_CHOICES, null=True, blank=True)
    item_approval_status = models.CharField(max_length=20, choices=ITEM_APPROVAL_STATUS_CHOICES, null=True, blank=True)
    assigned_to = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_out_inspection_items_assigned"
    )
    target_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    photo = models.FileField(upload_to="checkin_checkout/check_out_inspection_items/", max_length=500, null=True, blank=True)
    remarks = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_out_inspection_items_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "check_out_inspection_item"
        ordering = ["-created_at"]
        verbose_name = "Check-Out Inspection Item"
        verbose_name_plural = "Check-Out Inspection Items"

    def __str__(self):
        return f"{self.item_name} ({self.category}) for CheckOut {self.check_out_id}"

    def create(
        self,
        check_out_id: int,
        category: str,
        item_name: str,
        inspection_status: str,
        severity: str = None,
        repair_status: str = None,
        item_approval_status: str = None,
        assigned_to_id: int = None,
        target_date=None,
        cost=None,
        remarks: str = "",
        created_by: int = None,
    ) -> int:
        self.check_out_id = check_out_id
        self.category = category
        self.item_name = item_name
        self.inspection_status = inspection_status
        self.severity = severity
        self.repair_status = repair_status
        self.item_approval_status = item_approval_status
        self.assigned_to_id = assigned_to_id
        self.target_date = target_date
        self.cost = cost
        self.remarks = remarks
        self.created_by_id = created_by
        self.save()
        return self.check_out_inspection_item_id

    @staticmethod
    def get_all_for_check_out(check_out_id: int):
        return CheckOutInspectionItem.objects.filter(
            check_out_id=check_out_id, is_active=True
        ).values(
            "check_out_inspection_item_id", "category", "item_name", "inspection_status",
            "severity", "repair_status", "item_approval_status", "assigned_to_id", "assigned_to__name",
            "target_date", "cost", "photo", "remarks", "created_at",
        )

    @staticmethod
    def update(
        check_out_inspection_item_id: int,
        category: str = None,
        item_name: str = None,
        inspection_status: str = None,
        severity: str = None,
        repair_status: str = None,
        item_approval_status: str = None,
        assigned_to_id: int = None,
        target_date=None,
        cost=None,
        remarks: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            item = CheckOutInspectionItem.objects.get(check_out_inspection_item_id=check_out_inspection_item_id)
        except CheckOutInspectionItem.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Inspection Item Id: {check_out_inspection_item_id}")

        if category is not None:
            item.category = category
        if item_name is not None:
            item.item_name = item_name
        if inspection_status is not None:
            item.inspection_status = inspection_status
        if severity is not None:
            item.severity = severity
        if repair_status is not None:
            item.repair_status = repair_status
        if item_approval_status is not None:
            item.item_approval_status = item_approval_status
        if assigned_to_id is not None:
            item.assigned_to_id = assigned_to_id
        if target_date is not None:
            item.target_date = target_date
        if cost is not None:
            item.cost = cost
        if remarks is not None:
            item.remarks = remarks

        item.save()
        return item.check_out_inspection_item_id

    @staticmethod
    def delete(check_out_inspection_item_id: int) -> None:
        CheckOutInspectionItem.objects.filter(
            check_out_inspection_item_id=check_out_inspection_item_id
        ).update(is_active=False)
