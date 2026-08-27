from django.db import migrations


def backfill_property_type(apps, schema_editor):
    Building = apps.get_model('property', 'Building')
    Property = apps.get_model('property', 'Property')

    for building in Building.objects.filter(is_active=True):
        types = set(
            Property.objects.filter(
                building_id=building.building_id, is_active=True
            ).values_list('rental_type', flat=True)
        )
        # Only backfill when every active unit under this building agrees on
        # one type. Buildings with mixed types (an artifact of the original
        # text-based backfill grouping ambiguous/placeholder building names)
        # or no units at all are left null and are not constrained.
        if len(types) == 1:
            building.property_type = types.pop()
            building.save(update_fields=['property_type'])


def noop_reverse(apps, schema_editor):
    Building = apps.get_model('property', 'Building')
    Building.objects.update(property_type=None)


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0010_building_property_type'),
    ]

    operations = [
        migrations.RunPython(backfill_property_type, noop_reverse),
    ]
