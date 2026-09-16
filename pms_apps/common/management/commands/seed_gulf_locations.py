from django.core.management.base import BaseCommand

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
