from django.contrib import admin
from DHIS import models as dhis_models


# Register your models here.
class OrganisationUnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'ward', 'organisation_unit_name','organisation_uid', 'facility')
    autocomplete_fields = ["ward"]
    search_fields = ['organisation_unit_name']


class AttributeOptionComboAdmin(admin.ModelAdmin):
    list_display = ('id', 'attribute_option_combo_uid',)
    search_fields = ['attribute_option_combo_uid']


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('id', 'attribute_option_combo', 'dataset_name', 'dataset_uid')
    search_fields = ['dataset_name']


class DataElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'dataset','data_element_name','data_element_option', 'data_element_uid')
    search_fields = ['data_element_name']


class CategoryOptionComboAdmin(admin.ModelAdmin):
    list_display = ('id','category_option_combo_name', 'category_option_combo_uid')
    search_fields = ['category_option_combo_uid']


class CategoryOptionComboDataElementMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_element','category_option_combo')
    autocomplete_fields = ['category_option_combo']


admin.site.register(dhis_models.OrganisationUnit, OrganisationUnitAdmin)
admin.site.register(dhis_models.AttributeOptionCombo, AttributeOptionComboAdmin)
admin.site.register(dhis_models.Dataset, DatasetAdmin)
admin.site.register(dhis_models.DataElement, DataElementAdmin)
admin.site.register(dhis_models.CategoryOptionCombo, CategoryOptionComboAdmin)
admin.site.register(dhis_models.CategoryOptionComboDataElementMapping, CategoryOptionComboDataElementMappingAdmin)
