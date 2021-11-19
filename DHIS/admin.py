from django.contrib import admin
from DHIS import models as dhis_models


# Register your models here.
class DataElementAdmin(admin.ModelAdmin):
    list_display = ('id','data_element_sys_name','data_element_name', 'data_element_uid', 'payload_type')
    search_fields = ['data_element_name']


class CategoryOptionComboAdmin(admin.ModelAdmin):
    list_display = ('id','category_option_combo_name', 'category_option_combo_uid')
    search_fields = ['category_option_combo_uid']


class CategoryOptionComboDataElementMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_element','category_option_combo')
    autocomplete_fields = ['category_option_combo']

admin.site.register(dhis_models.DataElement, DataElementAdmin)
admin.site.register(dhis_models.CategoryOptionCombo, CategoryOptionComboAdmin)
admin.site.register(dhis_models.CategoryOptionComboDataElementMapping, CategoryOptionComboDataElementMappingAdmin)
