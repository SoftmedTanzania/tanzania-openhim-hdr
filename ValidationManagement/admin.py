from django.contrib import admin
from .models import TransactionSummary, TransactionSummaryLine, ValidationRule, FieldValidationMapping, PayloadThreshold


# Register your models here.
class FieldValidationMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_type','field','validation_rule')
    search_fields = ['message_type', ]


class PayloadThresholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'payload_description','payload_code','percentage_threshold')
    search_fields = ['payload_Description', ]


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


admin.site.register(TransactionSummary, TransactionSummaryAdmin)
admin.site.register(TransactionSummaryLine, TransactionSummaryLinesAdmin)
admin.site.register(ValidationRule, ValidationRuleAdmin)
admin.site.register(FieldValidationMapping, FieldValidationMappingAdmin)
admin.site.register(PayloadThreshold, PayloadThresholdAdmin)