from django.contrib import admin
from NHIF import models as nhif_models


# Register your models here.
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('id', 'facility_hfr_code', 'claimed_amount','period','date' ,'computed_amount','accepted_amount',
                    'loan_deductions','other_deductions','paid_amount')
    search_fields = ['facility_hfr_code', ]

admin.site.register(nhif_models.Claims, ClaimAdmin)
