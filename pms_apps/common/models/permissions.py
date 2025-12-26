from django.db import models

class PropertyPermission(models.Model):
    permission_id = models.AutoField(
        primary_key=True,
        verbose_name="Permission Id"
    )
    property = models.BooleanField(
        verbose_name="Is Property Permitted",
        default=False
    )

    class Meta:
        db_table = "property_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (Property: {self.property})"

    def create(self,property: bool) -> int:
        self.property = property
        self.save()
        return self.permission_id

    @staticmethod
    def update(
        permission_id: int, 
        property: bool = None
        ) -> int:

        permission = PropertyPermission.objects.get(permission_id=permission_id)
        if property is not None:
            permission.property = property
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        PropertyPermission.objects.get(permission_id=permission_id).delete()

class AgreementTeamPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    agreement_team = models.BooleanField(default=False, verbose_name="Is Agreement Team Permitted")

    class Meta:
        db_table = "agreement_team_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (AgreementTeam: {self.agreement_team})"

    def create(self, agreement_team: bool) -> int:
        self.agreement_team = agreement_team
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, agreement_team: bool = None) -> int:
        permission = AgreementTeamPermission.objects.get(permission_id=permission_id)
        if agreement_team is not None:
            permission.agreement_team = agreement_team
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        AgreementTeamPermission.objects.get(permission_id=permission_id).delete()

class CollectionPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    collection = models.BooleanField(default=False, verbose_name="Is Collection Permitted")

    class Meta:
        db_table = "collection_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (Collection: {self.collection})"

    def create(self, collection: bool) -> int:
        self.collection = collection
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, collection: bool = None) -> int:
        permission = CollectionPermission.objects.get(permission_id=permission_id)
        if collection is not None:
            permission.collection = collection
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        CollectionPermission.objects.get(permission_id=permission_id).delete()

class FinancePermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    finance = models.BooleanField(default=False, verbose_name="Is Finance Permitted")

    class Meta:
        db_table = "finance_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (Finance: {self.finance})"

    def create(self, finance: bool) -> int:
        self.finance = finance
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, finance: bool = None) -> int:
        permission = FinancePermission.objects.get(permission_id=permission_id)
        if finance is not None:
            permission.finance = finance
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        FinancePermission.objects.get(permission_id=permission_id).delete()

class GenerateManagerPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    generate_manager = models.BooleanField(default=False, verbose_name="Is Generate Manager Permitted")

    class Meta:
        db_table = "generate_manager_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (GenerateManager: {self.generate_manager})"

    def create(self, generate_manager: bool) -> int:
        self.generate_manager = generate_manager
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, generate_manager: bool = None) -> int:
        permission = GenerateManagerPermission.objects.get(permission_id=permission_id)
        if generate_manager is not None:
            permission.generate_manager = generate_manager
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        GenerateManagerPermission.objects.get(permission_id=permission_id).delete()

class HRPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    hr = models.BooleanField(default=False, verbose_name="Is HR Permitted")

    class Meta:
        db_table = "hr_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (HR: {self.hr})"

    def create(self, hr: bool) -> int:
        self.hr = hr
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, hr: bool = None) -> int:
        permission = HRPermission.objects.get(permission_id=permission_id)
        if hr is not None:
            permission.hr = hr
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        HRPermission.objects.get(permission_id=permission_id).delete()

class ITPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    it = models.BooleanField(default=False, verbose_name="Is IT Permitted")

    class Meta:
        db_table = "it_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (IT: {self.it})"

    def create(self, it: bool) -> int:
        self.it = it
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, it: bool = None) -> int:
        permission = ITPermission.objects.get(permission_id=permission_id)
        if it is not None:
            permission.it = it
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        ITPermission.objects.get(permission_id=permission_id).delete()

class LeadPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    lead = models.BooleanField(default=False, verbose_name="Is Lead Permitted")

    class Meta:
        db_table = "lead_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (Lead: {self.lead})"

    def create(self, lead: bool) -> int:
        self.lead = lead
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, lead: bool = None) -> int:
        permission = LeadPermission.objects.get(permission_id=permission_id)
        if lead is not None:
            permission.lead = lead
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        LeadPermission.objects.get(permission_id=permission_id).delete()

class LegalPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    legal = models.BooleanField(default=False, verbose_name="Is Legal Permitted")

    class Meta:
        db_table = "legal_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (Legal: {self.legal})"

    def create(self, legal: bool) -> int:
        self.legal = legal
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, legal: bool = None) -> int:
        permission = LegalPermission.objects.get(permission_id=permission_id)
        if legal is not None:
            permission.legal = legal
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        LegalPermission.objects.get(permission_id=permission_id).delete()

class MaintenancePermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    maintenance = models.BooleanField(default=False, verbose_name="Is Maintenance Permitted")

    class Meta:
        db_table = "maintenance_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (Maintenance: {self.maintenance})"

    def create(self, maintenance: bool) -> int:
        self.maintenance = maintenance
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, maintenance: bool = None) -> int:
        permission = MaintenancePermission.objects.get(permission_id=permission_id)
        if maintenance is not None:
            permission.maintenance = maintenance
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        MaintenancePermission.objects.get(permission_id=permission_id).delete()

class MarketingPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    marketing = models.BooleanField(default=False, verbose_name="Is Marketing Permitted")

    class Meta:
        db_table = "marketing_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (Marketing: {self.marketing})"

    def create(self, marketing: bool) -> int:
        self.marketing = marketing
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, marketing: bool = None) -> int:
        permission = MarketingPermission.objects.get(permission_id=permission_id)
        if marketing is not None:
            permission.marketing = marketing
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        MarketingPermission.objects.get(permission_id=permission_id).delete()

class OwnerPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    owner = models.BooleanField(default=False, verbose_name="Is Owner Permitted")

    class Meta:
        db_table = "owner_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (Owner: {self.owner})"

    def create(self, owner: bool) -> int:
        self.owner = owner
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, owner: bool = None) -> int:
        permission = OwnerPermission.objects.get(permission_id=permission_id)
        if owner is not None:
            permission.owner = owner
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        OwnerPermission.objects.get(permission_id=permission_id).delete()

class ReceptionPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    reception = models.BooleanField(default=False, verbose_name="Is Reception Permitted")

    class Meta:
        db_table = "reception_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (Reception: {self.reception})"

    def create(self, reception: bool) -> int:
        self.reception = reception
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, reception: bool = None) -> int:
        permission = ReceptionPermission.objects.get(permission_id=permission_id)
        if reception is not None:
            permission.reception = reception
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        ReceptionPermission.objects.get(permission_id=permission_id).delete()

class StoreManagerPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    store_manager = models.BooleanField(default=False, verbose_name="Is Store Manager Permitted")

    class Meta:
        db_table = "store_manager_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (StoreManager: {self.store_manager})"

    def create(self, store_manager: bool) -> int:
        self.store_manager = store_manager
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, store_manager: bool = None) -> int:
        permission = StoreManagerPermission.objects.get(permission_id=permission_id)
        if store_manager is not None:
            permission.store_manager = store_manager
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        StoreManagerPermission.objects.get(permission_id=permission_id).delete()

class SupervisorPermission(models.Model):
    permission_id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    supervisor = models.BooleanField(default=False, verbose_name="Is Supervisor Permitted")

    class Meta:
        db_table = "supervisor_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (Supervisor: {self.supervisor})"

    def create(self, supervisor: bool) -> int:
        self.supervisor = supervisor
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, supervisor: bool = None) -> int:
        permission = SupervisorPermission.objects.get(permission_id=permission_id)
        if supervisor is not None:
            permission.supervisor = supervisor
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        SupervisorPermission.objects.get(permission_id=permission_id).delete()
