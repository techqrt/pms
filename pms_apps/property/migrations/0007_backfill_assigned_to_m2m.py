from django.db import migrations


def backfill(apps, schema_editor):
    Property = apps.get_model('property', 'Property')
    through = Property.assigned_to_new.through
    qs = Property.objects.exclude(assigned_to_id__isnull=True).only('property_id', 'assigned_to_id')
    batch = [
        through(property_id=prop.property_id, user_id=prop.assigned_to_id)
        for prop in qs.iterator(chunk_size=500)
    ]
    through.objects.bulk_create(batch, ignore_conflicts=True)


def unbackfill(apps, schema_editor):
    Property = apps.get_model('property', 'Property')
    Property.assigned_to_new.through.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_add_property_assigned_to_m2m'),
    ]

    operations = [
        migrations.RunPython(backfill, unbackfill),
    ]
