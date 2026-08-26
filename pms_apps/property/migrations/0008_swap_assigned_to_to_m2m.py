from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_backfill_assigned_to_m2m'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='assigned_to',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='assigned_to_new',
            new_name='assigned_to',
        ),
    ]
