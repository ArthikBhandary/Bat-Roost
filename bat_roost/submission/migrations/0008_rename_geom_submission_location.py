# Generated by Django 3.2 on 2021-06-26 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0007_rename_location_submission_geom'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='geom',
            new_name='location',
        ),
    ]