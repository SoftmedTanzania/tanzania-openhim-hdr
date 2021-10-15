from django.contrib import admin
from .models import ServiceReceived, ServiceReceivedItems, DeathByDiseaseCaseAtFacility, DeathByDiseaseCaseAtFacilityItems, \
    DeathByDiseaseCaseNotAtFacility, DeathByDiseaseCaseNotAtFacilityItems, BedOccupancy, BedOccupancyItems, \
    RevenueReceived, RevenueReceivedItems, BedOccupancyReport
from UserManagement import models as user_management_models
from django.contrib.admin import helpers

# Register your models here.
class ServiceReceivedAdmin(admin.ModelAdmin):
    list_display = ('id', 'org_name', 'facility_hfr_code')
    search_fields = ['org_name', ]


class ServiceReceivedItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_received', 'department_name','department_id', 'patient_id','gender',
                    'date_of_birth','med_svc_code','icd_10_code','service_date','service_provider_ranking_id','visit_type')
    search_fields = ['service_received', ]


class DeathByDiseaseCaseAtFacilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'org_name', 'facility_hfr_code')
    search_fields = ['org_name', ]


class DeathByDiseaseCaseAtFacilityItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'death_by_disease_case_at_facility', 'ward_name','ward_id','patient_id','first_name', 'middle_name','last_name','gender',
                    'date_of_birth','icd_10_code','date_death_occurred')
    search_fields = ['ward_name',]


class DeathByDiseaseCaseNotAtFacilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'org_name', 'facility_hfr_code')
    search_fields = ['org_name', ]


class DeathByDiseaseCaseNotAtFacilityItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'death_by_disease_case_not_at_facility', 'place_of_death_id','gender',
                    'date_of_birth', 'icd_10_code','date_death_occurred','death_id')
    search_fields = ['place_of_death_id', ]


class BedOccupancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'org_name', 'facility_hfr_code')
    search_fields = ['org_name', ]


class BedOccupancyItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'bed_occupancy', 'patient_id','admission_date','discharge_date','ward_name','ward_id')
    search_fields = ['ward_name', ]


class RevenueReceivedAdmin(admin.ModelAdmin):
    list_display = ('id', 'org_name', 'facility_hfr_code')
    search_fields = ['org_name', ]


class RevenueReceivedItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'revenue_received', 'system_trans_id','transaction_date','patient_id','gender',
                    'date_of_birth','med_svc_code','payer_id','exemption_category_id','billed_amount','waived_amount',
                    'service_provider_ranking_id')
    search_fields = ['payer_id', ]


class BedOccupancyReportAdmin(admin.ModelAdmin):
    list_display = ('id','bed_occupancy', 'facility_hfr_code','patient_id', 'ward_id', 'ward_name', 'admission_date', 'date')


admin.site.register(ServiceReceived, ServiceReceivedAdmin)
admin.site.register(ServiceReceivedItems, ServiceReceivedItemsAdmin)
admin.site.register(DeathByDiseaseCaseAtFacility, DeathByDiseaseCaseAtFacilityAdmin)
admin.site.register(DeathByDiseaseCaseAtFacilityItems, DeathByDiseaseCaseAtFacilityItemsAdmin)
admin.site.register(DeathByDiseaseCaseNotAtFacility, DeathByDiseaseCaseNotAtFacilityAdmin)
admin.site.register(DeathByDiseaseCaseNotAtFacilityItems, DeathByDiseaseCaseNotAtFacilityItemsAdmin)
admin.site.register(BedOccupancy, BedOccupancyAdmin)
admin.site.register(BedOccupancyItems, BedOccupancyItemsAdmin)
admin.site.register(RevenueReceived, RevenueReceivedAdmin)
admin.site.register(RevenueReceivedItems, RevenueReceivedItemsAdmin)
admin.site.register(BedOccupancyReport, BedOccupancyReportAdmin)

