# Generated by Django 3.2.4 on 2021-11-03 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DHIS', '0004_auto_20211103_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryoptioncombo',
            name='category_option_combo_sys_name',
        ),
        migrations.AlterField(
            model_name='dataelement',
            name='date_element_sys_name',
            field=models.CharField(choices=[('claimed_amount', 'Claimed Amount'), ('computed_amount', 'Computed Amount'), ('accepted_amount', 'Accepted Amount'), ('loan_deductions', 'Loan Deductions'), ('other_deductions', 'Other Deductions'), ('paid_amount', 'Paid Amount')], max_length=30),
        ),
    ]
