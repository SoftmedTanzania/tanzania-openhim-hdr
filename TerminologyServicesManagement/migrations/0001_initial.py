# Generated by Django 3.2.4 on 2021-09-28 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('MasterData', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPTCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpt_code', models.CharField(max_length=255)),
                ('cpt_description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'CPT Code',
                'db_table': 'CPTCodes',
            },
        ),
        migrations.CreateModel(
            name='CPTCodeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'CPT Code Categories',
                'db_table': 'CPTCodeCategories',
            },
        ),
        migrations.CreateModel(
            name='ICD10Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icd10_code', models.CharField(max_length=255)),
                ('icd10_description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'ICD10 Codes',
                'db_table': 'ICD10Codes',
            },
        ),
        migrations.CreateModel(
            name='ICD10CodeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'ICD10 Code Categories',
                'db_table': 'ICD10CodeCategories',
            },
        ),
        migrations.CreateModel(
            name='ICD10SubCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icd10_sub_code', models.CharField(max_length=255)),
                ('icd10_sub_code_description', models.CharField(max_length=255)),
                ('icd10_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='TerminologyServicesManagement.icd10code')),
            ],
            options={
                'verbose_name_plural': 'ICD10 SubCodes',
                'db_table': 'ICD10SubCodes',
            },
        ),
        migrations.CreateModel(
            name='ICD10CodeSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('icd_10_code_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='TerminologyServicesManagement.icd10codecategory')),
            ],
            options={
                'verbose_name_plural': 'ICD10 Code Sub Categories',
                'db_table': 'ICD10CodeSubCategories',
            },
        ),
        migrations.AddField(
            model_name='icd10code',
            name='icd_10_code_sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='TerminologyServicesManagement.icd10codesubcategory'),
        ),
        migrations.CreateModel(
            name='CPTCodeSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('cpt_code_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='TerminologyServicesManagement.cptcodecategory')),
            ],
            options={
                'verbose_name_plural': 'CPT Code Sub Categories',
                'db_table': 'CPTCodeSubCategories',
            },
        ),
        migrations.CreateModel(
            name='CPTCodesMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_code', models.CharField(max_length=255)),
                ('cpt_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='TerminologyServicesManagement.cptcode')),
                ('facility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MasterData.facility')),
            ],
            options={
                'db_table': 'CPTCodesMappings',
            },
        ),
        migrations.AddField(
            model_name='cptcode',
            name='cpt_code_sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='TerminologyServicesManagement.cptcodesubcategory'),
        ),
    ]
