from django.contrib import admin
from django import forms
from .models import TransactionSummary, TransactionSummaryLine, ValidationRule, FieldValidationMapping, \
    PayloadThreshold, PayloadFieldMapping

# Register your models here.
# class FieldValidationMappingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'message_type','field','validation_rule')
#     search_fields = ['message_type', ]
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "message_type":
#             kwargs["queryset"] = PayloadFieldMapping.objects.filter(message_type=self.message_type)
#         return super(FieldValidationMappingAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class PayloadThresholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'payload_description','payload_code','percentage_threshold')
    search_fields = ['payload_Description', ]


class TransactionSummaryAdmin(admin.ModelAdmin):
    list_display = ('id','transaction_date_time','message_type','org_name','facility_hfr_code',
                    'total_passed','total_failed','is_active')
    search_fields = ['facility_hfr_code',]


class TransactionSummaryLinesAdmin(admin.ModelAdmin):
    list_display = ('id','transaction','payload_object','transaction_status',
                    'error_message')
    search_fields = []


class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = ('id','description','rule_name')
    search_fields = ['description',]


class PayloadFieldMappingAdmin(admin.ModelAdmin):
    list_display = ('id','message_type','field')
    search_fields = ['message_type',]

    # def has_delete_permission(self, request, obj=None):
    #     return False

admin.site.register(TransactionSummary, TransactionSummaryAdmin)
admin.site.register(TransactionSummaryLine, TransactionSummaryLinesAdmin)
admin.site.register(ValidationRule, ValidationRuleAdmin)
# admin.site.register(FieldValidationMapping, FieldValidationMappingAdmin)
admin.site.register(PayloadThreshold, PayloadThresholdAdmin)
# admin.site.register(PayloadFieldMapping, PayloadFieldMappingAdmin)