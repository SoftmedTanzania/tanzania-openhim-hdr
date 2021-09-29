from django.contrib import admin
from .models import  ICD10CodeCategory,ICD10CodeSubCategory, ICD10Code, ICD10SubCode, CPTCodeCategory, \
    CPTCodeSubCategory, CPTCode


# Register your models here.
class ICD10CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ['description', ]


class ICD10SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'icd10_code_category','description')
    search_fields = ['description', ]


class CPTCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ['description', ]


class CPTSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cpt_code_category','description')
    search_fields = ['description', ]


class CPTCodeAdmin(admin.ModelAdmin):
    list_display = ('cpt_code_sub_category','cpt_code', 'cpt_description')
    search_fields = ['cpt_description', ]


class ICD10SubCodeMappingAdmin(admin.ModelAdmin):
    list_display = ('icd10_code', 'icd10_sub_code', 'icd10_sub_code_description')
    search_fields = ['icd10_sub_code_description', ]


class ICD10MappingAdmin(admin.ModelAdmin):
    list_display = ('icd10_code_sub_category', 'icd10_code', 'icd10_description')
    search_fields = ['icd10_description', ]


admin.site.register(ICD10CodeCategory, ICD10CategoryAdmin)
admin.site.register(ICD10CodeSubCategory, ICD10SubCategoryAdmin)
admin.site.register(ICD10Code, ICD10MappingAdmin)
admin.site.register(ICD10SubCode, ICD10SubCodeMappingAdmin),
admin.site.register(CPTCodeCategory, CPTCategoryAdmin)
admin.site.register(CPTCodeSubCategory, CPTSubCategoryAdmin)
admin.site.register(CPTCode, CPTCodeAdmin)
