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

    data_element_name = models.CharField(max_length=255)
    data_element_uid = models.CharField(max_length=255)

    class Meta:
        db_table = "data_elements"


class CategoryOptionCombo(models.Model):
    def __str__(self):
        return "%d" % self.id

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
