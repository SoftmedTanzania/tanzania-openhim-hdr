from django.contrib import admin
from .models import TransactionSummary,ValidationRule , FieldValidationMapping, TransactionSummaryLine, \
    ServiceReceived, ServiceReceivedItems, DeathByDiseaseCaseAtFacility, DeathByDiseaseCaseAtFacilityItems, \
    DeathByDiseaseCaseNotAtFacility, DeathByDiseaseCaseNotAtFacilityItems, BedOccupancy, BedOccupancyItems, \
    RevenueReceived, RevenueReceivedItems, PayloadThreshold
from django.contrib.admin import helpers

# Register your models here.
class TransactionSummaryAdmin(admin.ModelAdmin):
    list_display = ('id','transaction_date_time','message_type','org_name','facility_hfr_code',
                    'total_passed','total_failed','facility_hfr_code')
    search_fields = ['facility_hfr_code',]


class TransactionSummaryLinesAdmin(admin.ModelAdmin):
    list_display = ('id','transaction','payload_object','transaction_status',
                    'error_message')
    search_fields = []


class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = ('id','description','rule_name')
    search_fields = ['description',]

    def has_delete_permission(self, request, obj=None):
        return False

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
    list_display = ('id', 'death_by_disease_case_at_facility', 'ward_name','ward_id','patient_id', 'gender',
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


class FieldValidationMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_type','field','validation_rule')
    search_fields = ['message_type', ]


class PayloadThresholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'payload_description','payload_code','percentage_threshold')
    search_fields = ['payload_Description', ]


admin.site.register(TransactionSummary, TransactionSummaryAdmin)
admin.site.register(TransactionSummaryLine, TransactionSummaryLinesAdmin)
admin.site.register(ValidationRule, ValidationRuleAdmin)
admin.site.register(FieldValidationMapping, FieldValidationMappingAdmin)
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
admin.site.register(PayloadThreshold, PayloadThresholdAdmin)

