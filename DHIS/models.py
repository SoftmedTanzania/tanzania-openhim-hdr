from django.db import models
from MasterData import models as master_data_models



# Create your models here.
class OrganisationUnit(models.Model):
    def __str__(self):
        return "%d" % self.id

    organisation_unit_name = models.CharField(max_length=255)
    organisation_uid = models.CharField(max_length=255)
    facility = models.ForeignKey(master_data_models.Facility, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "organisation_units"
        verbose_name_plural = "1. Organization Units"


class DataElement(models.Model):
    def __str__(self):
        return "%s" % self.data_element_name

    nhif_claims = 'nhif_claims'
    death_within_facility = 'death_within_facility'

    claimed_amount = 'claimed_amount'
    computed_amount = 'computed_amount'
    accepted_amount = 'accepted_amount'
    loan_deductions = 'loan_deductions'
    other_deductions = 'other_deductions'
    paid_amount = 'paid_amount'

    reporting_date = 'reporting_date'
    date_death_occurred = 'date_death_occurred'
    client_name = 'client_name'
    gender = 'gender'
    date_of_birth = 'date_of_birth'
    place_of_death = 'place_of_death'
    immediate_cause_of_death = 'immediate_cause_of_death'
    underlying_cause_of_death = 'underlying_cause_of_death'

    DATA_ELEMENT_TYPE_CHOICES = (
        (claimed_amount, 'Claimed Amount'),
        (computed_amount, 'Computed Amount'),
        (accepted_amount, 'Accepted Amount'),
        (loan_deductions, 'Loan Deductions'),
        (other_deductions, 'Other Deductions'),
        (paid_amount, 'Paid Amount'),

        (reporting_date, 'Reporting Date'),
        (date_death_occurred, 'Date Death Occurred'),
        (client_name, 'Client Name'),
        (gender, 'Gender'),
        (date_of_birth, 'Date of Birth'),
        (place_of_death, 'Place of Death'),
        (immediate_cause_of_death, 'Immediate Cause of Death'),
        (underlying_cause_of_death, 'Underlying Cause of Death'),
    )

    PAYLOAD_TYPE = (
        (nhif_claims, 'NHIF Claims'),
        (death_within_facility, 'Death Within Facility')
    )

    payload_type = models.CharField(max_length=100, choices=PAYLOAD_TYPE)
    data_element_sys_name = models.CharField(max_length=30, choices=DATA_ELEMENT_TYPE_CHOICES)
    data_element_name = models.CharField(max_length=255)
    data_element_uid = models.CharField(max_length=255)

    class Meta:
        db_table = "data_elements"
        verbose_name_plural = "2. Data Elements"


class CategoryOptionCombo(models.Model):
    def __str__(self):
        return "%s" % self.category_option_combo_name

    category_option_combo_name = models.CharField(max_length=255)
    category_option_combo_uid = models.CharField(max_length=255)

    class Meta:
        db_table = "category_option_combo"
        verbose_name_plural = "3. Category Option Combo"



class CategoryOptionComboDataElementMapping(models.Model):
    def __str__(self):
        return "%d" % self.id

    data_element = models.ForeignKey(DataElement, on_delete=models.SET_NULL, null=True, blank=True)
    category_option_combo = models.ForeignKey(CategoryOptionCombo, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "category_option_combo_data_element_mapping"
        verbose_name_plural = "4. Category Option Combo Data Element Mapping"
