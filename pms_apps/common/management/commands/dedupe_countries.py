from collections import defaultdict

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from pms_apps.helper_apis.models.country import Country
from pms_apps.helper_apis.models.city import City
from pms_apps.lead.models.lead import Lead


class Command(BaseCommand):
    help = (
        "Merge duplicate Country rows into one canonical row: re-point any Lead/City "
        "rows at the canonical row (de-duping matching cities by name along the way) "
        "and delete the duplicate. Two ways to find duplicates:\n"
        "  - automatic: rows whose name is identical once trimmed/lowercased "
        "(e.g. 'UAE' vs 'uae ')\n"
        "  - manual: pairs you know are the same country under different spellings "
        "(e.g. 'UAE' vs 'United Arab Emirates'), passed via --merge dup_id=keep_id\n"
        "Without --yes this only prints what it would do."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes", action="store_true",
            help="Required to actually merge/delete. Without it, only a dry-run report is shown.",
        )
        parser.add_argument(
            "--merge", action="append", default=[],
            help=(
                "Manually merge one duplicate country into a canonical one: "
                "dup_id=keep_id (e.g. --merge 47=3). Repeatable."
            ),
        )

    def handle(self, *args, **kwargs):
        manual_pairs = self._parse_manual_pairs(kwargs["merge"])

        groups = defaultdict(list)
        for country in Country.objects.all().order_by("country_id"):
            key = country.name.strip().lower()
            groups[key].append(country)
        auto_groups = [v for v in groups.values() if len(v) > 1]

        pairs = []
        for group in auto_groups:
            canonical = group[0]
            for dup in group[1:]:
                pairs.append((dup, canonical))
        pairs.extend(manual_pairs)

        if not pairs:
            self.stdout.write(self.style.SUCCESS("No duplicate countries found."))
            return

        for dup, canonical in pairs:
            self.stdout.write(
                f"Will merge id={dup.country_id} name={dup.name!r} "
                f"into id={canonical.country_id} name={canonical.name!r}"
            )

        if not kwargs["yes"]:
            self.stdout.write(self.style.WARNING(
                "Dry run only - nothing changed. Re-run with --yes to merge these."
            ))
            return

        with transaction.atomic():
            for dup, canonical in pairs:
                self._merge(dup, canonical)

        self.stdout.write(self.style.SUCCESS("Duplicate countries merged."))

    def _parse_manual_pairs(self, raw_pairs):
        pairs = []
        for raw in raw_pairs:
            try:
                dup_id_str, keep_id_str = raw.split("=")
                dup_id, keep_id = int(dup_id_str), int(keep_id_str)
            except ValueError:
                raise CommandError(f"--merge must look like dup_id=keep_id, got {raw!r}")
            try:
                dup = Country.objects.get(country_id=dup_id)
                canonical = Country.objects.get(country_id=keep_id)
            except Country.DoesNotExist:
                raise CommandError(f"--merge {raw}: no such Country id")
            pairs.append((dup, canonical))
        return pairs

    def _merge(self, dup, canonical):
        if canonical.name != canonical.name.strip():
            canonical.name = canonical.name.strip()
            canonical.save()

        leads_moved = Lead.objects.filter(country=dup).update(country=canonical)
        self.stdout.write(f"  Re-pointed {leads_moved} leads' country to id={canonical.country_id}")

        canonical_cities_by_key = {
            c.name.strip().lower(): c for c in City.objects.filter(country=canonical)
        }
        for city in City.objects.filter(country=dup):
            key = city.name.strip().lower()
            match = canonical_cities_by_key.get(key)
            if match:
                moved = Lead.objects.filter(city=city).update(city=match)
                self.stdout.write(
                    f"  City {city.name!r}: re-pointed {moved} leads to matching "
                    f"city id={match.city_id}, deleting duplicate city id={city.city_id}"
                )
                city.delete()
            else:
                city.country = canonical
                city.save()
                canonical_cities_by_key[key] = city
                self.stdout.write(f"  Moved city {city.name!r} to id={canonical.country_id}")

        dup.delete()
        self.stdout.write(f"  Deleted duplicate country id={dup.country_id}")
