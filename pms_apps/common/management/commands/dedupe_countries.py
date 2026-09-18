from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction

from pms_apps.helper_apis.models.country import Country
from pms_apps.helper_apis.models.city import City


class Command(BaseCommand):
    help = (
        "Find Country rows that are the same country under different spelling/casing/"
        "whitespace (e.g. 'UAE' vs 'UAE '), merge them into one canonical row, "
        "re-point any City rows at the canonical row, and delete the duplicates. "
        "Without --yes this only prints what it would do."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes", action="store_true",
            help="Required to actually merge/delete. Without it, only a dry-run report is shown.",
        )

    def handle(self, *args, **kwargs):
        groups = defaultdict(list)
        for country in Country.objects.all().order_by("country_id"):
            key = country.name.strip().lower()
            groups[key].append(country)

        duplicate_groups = {k: v for k, v in groups.items() if len(v) > 1}

        if not duplicate_groups:
            self.stdout.write(self.style.SUCCESS("No duplicate countries found."))
            return

        for key, countries in duplicate_groups.items():
            names = [repr(c.name) for c in countries]
            self.stdout.write(
                f"Duplicate group '{key}': "
                + ", ".join(f"id={c.country_id} name={n}" for c, n in zip(countries, names))
            )

        if not kwargs["yes"]:
            self.stdout.write(self.style.WARNING(
                "Dry run only - nothing changed. Re-run with --yes to merge these."
            ))
            return

        with transaction.atomic():
            for key, countries in duplicate_groups.items():
                canonical = countries[0]
                duplicates = countries[1:]
                if canonical.name != canonical.name.strip():
                    canonical.name = canonical.name.strip()
                    canonical.save()
                for dup in duplicates:
                    moved = City.objects.filter(country=dup).update(country=canonical)
                    self.stdout.write(
                        f"  Re-pointed {moved} cities from id={dup.country_id} to id={canonical.country_id}"
                    )
                    dup.delete()
                    self.stdout.write(f"  Deleted duplicate country id={dup.country_id}")

        self.stdout.write(self.style.SUCCESS("Duplicate countries merged."))
