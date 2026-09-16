from django.core.management.base import BaseCommand
from django.db import transaction

from pms_apps.lead.models.lead import Lead
from pms_apps.property.models.property import Property
from pms_apps.checkin_checkout.models.check_in import CheckIn
from pms_apps.checkin_checkout.models.check_out import CheckOut


class Command(BaseCommand):
    help = (
        "Delete all Lead, Property and CheckIn/CheckOut business records. "
        "Property is deleted first so its cascaded children (PropertyDetail, "
        "PropertyPhotos, PropertyAssignment, CheckIn, CheckOut and their "
        "documents/keys/payments) are removed before Lead, avoiding the "
        "PropertyDetail.landlord PROTECT constraint. Everything else "
        "(Users, Building, Country/City, HR/Finance/Marketing/etc.) is left untouched."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes", action="store_true",
            help="Skip the confirmation prompt and delete immediately.",
        )

    def handle(self, *args, **kwargs):
        counts = {
            "Property": Property.objects.count(),
            "CheckIn": CheckIn.objects.count(),
            "CheckOut": CheckOut.objects.count(),
            "Lead": Lead.objects.count(),
        }
        self.stdout.write("Records to be deleted:")
        for name, count in counts.items():
            self.stdout.write(f"  {name}: {count}")

        if not any(counts.values()):
            self.stdout.write(self.style.SUCCESS("Nothing to delete."))
            return

        if not kwargs["yes"]:
            confirm = input(
                "This will permanently delete ALL Lead, Property and CheckIn/CheckOut "
                "records (and their cascaded children). Type 'yes' to continue: "
            )
            if confirm.strip().lower() != "yes":
                self.stdout.write(self.style.WARNING("Aborted."))
                return

        with transaction.atomic():
            # Property cascades to PropertyDetail, PropertyPhotos, PropertyAssignment,
            # CheckIn, CheckOut and all CheckIn/CheckOut child tables.
            property_deleted = Property.objects.all().delete()
            lead_deleted = Lead.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted Property tree: {property_deleted}"))
        self.stdout.write(self.style.SUCCESS(f"Deleted Lead: {lead_deleted}"))
