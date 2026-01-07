from django.test import TestCase

# Create your tests here.
from pms_apps.helper_apis.models.country import Country
from pms_apps.helper_apis.models.city import City
from pms_apps.helper_apis.models.nationality import Nationality


def seed_master_data():
    # --------------------
    # Countries
    # --------------------
    country_names = [
        "India",
        "United States",
        "United Kingdom",
        "Canada",
        "Australia",
        "Germany",
        "France",
        "Japan",
        "Brazil",
        "UAE",
    ]

    countries = {}
    for name in country_names:
        country= Country.objects.create(name=name)
        countries[name] = country.country_id

    # --------------------
    # Cities (mapped to countries)
    # --------------------
    city_data = [
        ("Delhi", "India"),
        ("Mumbai", "India"),
        ("New York", "United States"),
        ("London", "United Kingdom"),
        ("Toronto", "Canada"),
        ("Sydney", "Australia"),
        ("Berlin", "Germany"),
        ("Paris", "France"),
        ("Tokyo", "Japan"),
        ("Dubai", "UAE"),
    ]

    for city_name, country_name in city_data:
        City.objects.get_or_create(
            name=city_name,
            country_id=countries[country_name]
        )

    # --------------------
    # Nationalities
    # --------------------
    nationality_names = [
        "Indian",
        "American",
        "British",
        "Canadian",
        "Australian",
        "German",
        "French",
        "Japanese",
        "Brazilian",
        "Emirati",
    ]

    for name in nationality_names:
        Nationality.objects.get_or_create(name=name)

    print("✅ Seed data inserted successfully")
