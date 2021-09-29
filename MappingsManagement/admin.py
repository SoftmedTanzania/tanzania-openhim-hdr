from django.contrib import admin
from .models import PlaceOfDeathMapping, ServiceProviderRankingMapping,PayerMapping,ExemptionMapping, \
    GenderMapping, DepartmentMapping


# Register your models here.
class PlaceOfDeathMappingAdmin(admin.ModelAdmin):
    list_display = ('place_of_death','local_place_of_death_id',
                    'local_place_of_death_description','facility')
    search_fields = ['local_place_of_death_description', ]


class ServiceProviderRankingMappingAdmin(admin.ModelAdmin):
    list_display = ('service_provider_ranking','local_service_provider_ranking_id',
                    'local_service_provider_ranking_description','facility')
    search_fields = ['local_service_provider_ranking_description', ]


class ExemptionMappingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'exemption','local_exemption_id','local_exemption_description','facility')
    search_fields = ['local_exemption_description', ]


class GenderMappingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'gender','local_gender_description','facility')
    search_fields = ['local_gender_description', ]


class DepartmentMappingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'local_department_id', 'local_department_description', 'facility')
    search_fields = ['local_department_description', ]


class PayerMappingsAdmin(admin.ModelAdmin):
    list_display = ('id','payer','local_payer_id','local_payer_description', 'facility')
    search_fields = ['local_payer_description',]


admin.site.register(DepartmentMapping, DepartmentMappingsAdmin)
admin.site.register(PayerMapping, PayerMappingsAdmin)
admin.site.register(ExemptionMapping, ExemptionMappingsAdmin)
admin.site.register(GenderMapping, GenderMappingsAdmin)
admin.site.register(ServiceProviderRankingMapping, ServiceProviderRankingMappingAdmin)
admin.site.register(PlaceOfDeathMapping, PlaceOfDeathMappingAdmin)