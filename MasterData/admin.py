from django.contrib import admin
from MasterData.models import Department, Ward, Payer, Exemption, Facility, \
    Gender, ServiceProviderRanking\
    , PlaceOfDeath, Zone, Region, DistrictCouncil

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


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('id','description', 'facility_hfr_code','district_council','is_cpt_mapped','is_active')
    search_fields = ['description',]


class WardAdmin(admin.ModelAdmin):
    list_display = ('description','local_ward_id','local_ward_description', 'number_of_beds', 'department','facility')
    search_fields = ['local_ward_description']


class PayerAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    search_fields = ['description',]


class ExemptionAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    search_fields = ['description', ]


class GenderAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    search_fields = ['description', ]


class ServiceProviderRankingAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ['description', ]


class PlaceOfDeathAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ['description', ]


admin.site.register(Zone, ZoneAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(DistrictCouncil, DistrictCouncilAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(Payer, PayerAdmin)
admin.site.register(Exemption, ExemptionAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(ServiceProviderRanking, ServiceProviderRankingAdmin)
admin.site.register(PlaceOfDeath, PlaceOfDeathAdmin)

