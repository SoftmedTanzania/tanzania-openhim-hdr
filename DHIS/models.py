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


class DataElement(models.Model):
    def __str__(self):
        return "%s" % self.data_element_name

    claimed_amount = 'claimed_amount'
    computed_amount = 'computed_amount'
    accepted_amount = 'accepted_amount'
    loan_deductions = 'loan_deductions'
    other_deductions = 'other_deductions'
    paid_amount = 'paid_amount'

    DATA_ELEMENT_TYPE_CHOICES = (
        (claimed_amount, 'Claimed Amount'),
        (computed_amount, 'Computed Amount'),
        (accepted_amount, 'Accepted Amount'),
        (loan_deductions, 'Loan Deductions'),
        (other_deductions, 'Other Deductions'),
        (paid_amount, 'Paid Amount'),
    )

    data_element_sys_name = models.CharField(max_length=30, choices=DATA_ELEMENT_TYPE_CHOICES)
    data_element_name = models.CharField(max_length=255)
    data_element_uid = models.CharField(max_length=255)

    class Meta:
        db_table = "data_elements"


class CategoryOptionCombo(models.Model):
    def __str__(self):
        return "%s" % self.category_option_combo_name

    category_option_combo_name = models.CharField(max_length=255)
    category_option_combo_uid = models.CharField(max_length=255)

    class Meta:
        db_table = "category_option_combo"
        verbose_name_plural = "Category Option Combo"


class CategoryOptionComboDataElementMapping(models.Model):
    def __str__(self):
        return "%d" % self.id

    data_element = models.ForeignKey(DataElement, on_delete=models.SET_NULL, null=True, blank=True)
    category_option_combo = models.ForeignKey(CategoryOptionCombo, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "category_option_combo_data_element_mapping"
        verbose_name_plural = "Category Option Combo Data Element Mapping"
