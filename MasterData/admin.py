from django.contrib import admin
from MasterData.models import Department, Ward, Payer, Exemption, Facility, \
    ICD10Code, CPTCode,PayerMapping, ExemptionMapping, DepartmentMapping, Gender, GenderMapping, ServiceProviderRanking, \
    ServiceProviderRankingMapping, PlaceOfDeath, PlaceOfDeathMapping, Zone, Region, DistrictCouncil, CPTCodeCategory, \
    CPTCodeSubCategory, ICD10CodeCategory, ICD10CodeSubCategory, ICD10SubCode

# Register your models here.
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('id','description',)
    search_fields = ['description',]


class RegionAdmin(admin.ModelAdmin):
    list_display = ('id','zone', 'description',)
    search_fields = ['description', ]


class DistrictCouncilAdmin(admin.ModelAdmin):
    list_display = ('id', 'region', 'description',)
    search_fields = ['description', ]


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id','description',)
    search_fields = ['description',]


class DepartmentMappingsAdmin(admin.ModelAdmin):
    list_display = ('id','department','local_department_id', 'local_department_description', 'facility')
    search_fields = ['local_department_description',]


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('id','description', 'facility_hfr_code','district_council', 'is_active')
    search_fields = ['description',]


class WardAdmin(admin.ModelAdmin):
    list_display = ('description','local_ward_id','local_ward_description', 'number_of_beds', 'department','facility')
    search_fields = ['local_ward_description']


class PayerAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    search_fields = ['description',]


class PayerMappingsAdmin(admin.ModelAdmin):
    list_display = ('id','payer','local_payer_id','local_payer_description', 'facility')
    search_fields = ['local_payer_description',]


class ExemptionAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    search_fields = ['description', ]


class ExemptionMappingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'exemption','local_exemption_id','local_exemption_description','facility')
    search_fields = ['local_exemption_description', ]


class GenderAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    search_fields = ['description', ]


class GenderMappingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'gender','local_gender_description','facility')
    search_fields = ['local_gender_description', ]


class ICD10CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ['description', ]


class ICD10SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'icd_10_code_category','description')
    search_fields = ['description', ]


class ICD10MappingAdmin(admin.ModelAdmin):
    list_display = ('icd_10_code_sub_category','icd10_code', 'icd10_description')
    search_fields = ['icd10_description', ]


class ICD10SubCodeMappingAdmin(admin.ModelAdmin):
    list_display = ('icd10_code','icd10_sub_code', 'icd10_sub_code_description')
    search_fields = ['icd10_sub_code_description', ]


class CPTCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ['description', ]


class CPTSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cpt_code_category','description')
    search_fields = ['description', ]


class CPTCodeAdmin(admin.ModelAdmin):
    list_display = ('cpt_code_sub_category','cpt_code', 'cpt_description')
    search_fields = ['cpt_description', ]


class ServiceProviderRankingAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ['description', ]


class ServiceProviderRankingMappingAdmin(admin.ModelAdmin):
    list_display = ('service_provider_ranking','local_service_provider_ranking_id',
                    'local_service_provider_ranking_description','facility')
    search_fields = ['local_service_provider_ranking_description', ]


class PlaceOfDeathAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ['description', ]


class PlaceOfDeathMappingAdmin(admin.ModelAdmin):
    list_display = ('place_of_death','local_place_of_death_id',
                    'local_place_of_death_description','facility')
    search_fields = ['local_place_of_death_description', ]


admin.site.register(Zone, ZoneAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(DistrictCouncil, DistrictCouncilAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartmentMapping, DepartmentMappingsAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(Payer, PayerAdmin)
admin.site.register(PayerMapping, PayerMappingsAdmin)
admin.site.register(Exemption, ExemptionAdmin)
admin.site.register(ExemptionMapping, ExemptionMappingsAdmin)
admin.site.register(CPTCode, CPTCodeAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(GenderMapping, GenderMappingsAdmin)
admin.site.register(ServiceProviderRanking, ServiceProviderRankingAdmin)
admin.site.register(ServiceProviderRankingMapping, ServiceProviderRankingMappingAdmin)
admin.site.register(PlaceOfDeath, PlaceOfDeathAdmin)
admin.site.register(PlaceOfDeathMapping, PlaceOfDeathMappingAdmin)
admin.site.register(ICD10CodeCategory, ICD10CategoryAdmin)
admin.site.register(ICD10CodeSubCategory, ICD10SubCategoryAdmin)
admin.site.register(ICD10Code, ICD10MappingAdmin)
admin.site.register(ICD10SubCode, ICD10SubCodeMappingAdmin),
admin.site.register(CPTCodeCategory, CPTCategoryAdmin)
admin.site.register(CPTCodeSubCategory, CPTSubCategoryAdmin)

