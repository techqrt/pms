from django.core.management.base import BaseCommand
from django.db import connection

from pms_apps.helper_apis.models.country import Country
from pms_apps.helper_apis.models.city import City

GULF_LOCATIONS = {
    "Oman": ["Muscat", "Salalah", "Sohar", "Nizwa"],
    "UAE": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Ras Al Khaimah", "Fujairah"],
    "Kuwait": ["Kuwait City", "Hawalli", "Salmiya", "Al Ahmadi"],
    "Saudi Arabia": ["Riyadh", "Jeddah", "Dammam", "Mecca", "Medina"],
    "Qatar": ["Doha", "Al Wakrah", "Al Rayyan"],
    "Bahrain": ["Manama", "Riffa", "Muharraq"],
}


class Command(BaseCommand):
    help = "Seed Country/City records for Oman, UAE, Kuwait, Saudi Arabia, Qatar and Bahrain."

    def handle(self, *args, **kwargs):
        self._fix_sequence("country", "country_id")
        self._fix_sequence("city", "city_id")

        for country_name, cities in GULF_LOCATIONS.items():
            country, created = Country.objects.get_or_create(name=country_name)
            self.stdout.write(
                f"{'Created' if created else 'Found'} country: {country_name}"
            )
            for city_name in cities:
                city, city_created = City.objects.get_or_create(
                    name=city_name, country=country
                )
                self.stdout.write(
                    f"  {'Created' if city_created else 'Found'} city: {city_name}"
                )

        self.stdout.write(self.style.SUCCESS("Gulf countries/cities seeded."))

    def _fix_sequence(self, table, pk_column):
        """Realign the Postgres auto-increment sequence with MAX(pk_column).

        Rows inserted with an explicit id (fixtures, manual INSERTs) leave the
        sequence behind, so the next get_or_create() insert collides on an
        id that's already taken. No-op on non-Postgres backends.
        """
        if connection.vendor != "postgresql":
            return
        quoted_table = connection.ops.quote_name(table)
        quoted_pk = connection.ops.quote_name(pk_column)
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT setval(pg_get_serial_sequence(%s, %s), "
                f"COALESCE((SELECT MAX({quoted_pk}) FROM {quoted_table}), 1), "
                f"(SELECT MAX({quoted_pk}) FROM {quoted_table}) IS NOT NULL)",
                [table, pk_column],
            )
