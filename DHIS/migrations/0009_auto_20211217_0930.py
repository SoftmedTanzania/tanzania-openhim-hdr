# Generated by Django 3.1.6 on 2021-12-17 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DHIS', '0008_alter_dataelement_data_element_sys_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoptioncombo',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='categoryoptioncombodataelementmapping',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='dataelement',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='organisationunit',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
