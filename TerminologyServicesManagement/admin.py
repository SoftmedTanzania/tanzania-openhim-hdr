from django.contrib import admin
from .models import  ICD10CodeCategory,ICD10CodeSubCategory, ICD10Code, ICD10SubCode, CPTCodeCategory, \
    CPTCodeSubCategory, CPTCode


# Register your models here.
class ICD10CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','identifier' ,'description')
    search_fields = ['description', ]


class ICD10SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','identifier','category_id','category','description')
    search_fields = ['description', ]


class ICD10CodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_category','sub_category_id','code','description')
    search_fields = ['description', ]


class ICD10SubCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code','code_id','sub_code', 'description')
    search_fields = ['description', ]


class CPTCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ['description', ]


class CPTSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_id','category','description')
    search_fields = ['description', ]


class CPTCodeAdmin(admin.ModelAdmin):
    list_display = ('id','sub_category_id','sub_category','code', 'description')
    search_fields = ['description', ]



admin.site.register(ICD10CodeCategory, ICD10CategoryAdmin)
admin.site.register(ICD10CodeSubCategory, ICD10SubCategoryAdmin)
admin.site.register(ICD10Code, ICD10CodeAdmin)
admin.site.register(ICD10SubCode, ICD10SubCodeAdmin)
admin.site.register(CPTCodeCategory, CPTCategoryAdmin)
admin.site.register(CPTCodeSubCategory, CPTSubCategoryAdmin)
admin.site.register(CPTCode, CPTCodeAdmin)
