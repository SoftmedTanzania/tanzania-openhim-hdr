from django.db import models
from MasterData import models as master_data_models



# Create your models here.
class OrganisationUnit(models.Model):
    def __str__(self):
        return "%d" % self.id

    ward = models.ForeignKey(master_data_models.Ward, on_delete=models.SET_NULL, null=True, blank=True)
    organisation_unit_name = models.CharField(max_length=255)
    organisation_uid = models.CharField(max_length=255)
    facility = models.ForeignKey(master_data_models.Facility, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "organisation_units"


class AttributeOptionCombo(models.Model):
    def __str__(self):
        return "%s" % self.attribute_option_combo_uid

    attribute_option_combo_uid = models.CharField(max_length=255)

    class Meta:
        db_table = "attribute_option_combo"
        verbose_name_plural = "Attribute Option Combo"


class Dataset(models.Model):
    def __str__(self):
        return "%s" % self.dataset_name

    attribute_option_combo = models.ForeignKey(AttributeOptionCombo, on_delete=models.SET_NULL, null=True, blank=True)
    dataset_name = models.CharField(max_length=255)
    dataset_uid = models.CharField(max_length=255)

    class Meta:
        db_table = "datasets"


class DataElement(models.Model):
    def __str__(self):
        return "%s" % self.data_element_name


    DATA_ELEMENT_OPTIONS = (
    )

    dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, null=True, blank=True)
    data_element_name = models.CharField(max_length=255)
    data_element_uid = models.CharField(max_length=255)
    data_element_option = models.CharField(max_length=255, choices=DATA_ELEMENT_OPTIONS, unique=True)

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
