from django.db import migrations

UNASSIGNED_BUILDING_NAME = "Unassigned"


def backfill_buildings(apps, schema_editor):
    Property = apps.get_model('property', 'Property')
    PropertyDetail = apps.get_model('property', 'PropertyDetail')
    Building = apps.get_model('property', 'Building')

    detail_by_property_id = {
        d.property_id: d
        for d in PropertyDetail.objects.all()
    }

    groups = {}
    for prop in Property.objects.all():
        detail = detail_by_property_id.get(prop.property_id)
        name = (prop.building_details or '').strip()
        if not name and detail:
            name = (detail.building_name or '').strip()
        groups.setdefault(name, []).append((prop, detail))

    for name, entries in groups.items():
        building_name = name or UNASSIGNED_BUILDING_NAME

        address_source = next((d for _, d in entries if d is not None), None)

        building = Building.objects.create(
            name=building_name,
            address_line_1=getattr(address_source, 'address_line_1', '') or '',
            area_zone=getattr(address_source, 'area_zone', '') or '',
            city=getattr(address_source, 'city', '') or '',
            state=getattr(address_source, 'state', '') or '',
            country=getattr(address_source, 'country', '') or '',
            pincode=getattr(address_source, 'pincode', '') or '',
        )

        property_ids = [prop.property_id for prop, _ in entries]
        Property.objects.filter(property_id__in=property_ids).update(building_id=building.building_id)


def noop_reverse(apps, schema_editor):
    Property = apps.get_model('property', 'Property')
    Property.objects.update(building=None)

    Building = apps.get_model('property', 'Building')
    Building.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_property_building'),
    ]

    operations = [
        migrations.RunPython(backfill_buildings, noop_reverse),
    ]
