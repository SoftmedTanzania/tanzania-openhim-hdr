# Generated by Django 3.2.4 on 2021-11-03 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MasterData', '0002_facility_is_cpt_mapped'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='dhis_org_unit_uid',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
