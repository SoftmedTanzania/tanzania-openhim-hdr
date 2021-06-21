from django import forms
from .models import DepartmentMapping, ExemptionMapping, PayerMapping, Ward, GenderMapping,\
    ServiceProviderRankingMapping,PlaceOfDeathMapping, CPTCodesMapping


class DepartmentMappingForm(forms.ModelForm):

    class Meta:
        model = DepartmentMapping
        fields = ('department', 'local_department_id','local_department_description','facility')
        widgets = {'facility': forms.HiddenInput()}

class ExemptionMappingForm(forms.ModelForm):

    class Meta:
        model = ExemptionMapping
        fields = ('exemption', 'local_exemption_id','local_exemption_description','facility')
        widgets = {'facility': forms.HiddenInput()}


class PayerMappingForm(forms.ModelForm):

    class Meta:
        model = PayerMapping
        fields = ('payer', 'local_payer_id','local_payer_description','facility')
        widgets = {'facility': forms.HiddenInput()}


class WardMappingForm(forms.ModelForm):

    class Meta:
        model = Ward
        fields = ('description', 'local_ward_id','local_ward_description','number_of_beds','department','facility')
        widgets = {'facility': forms.HiddenInput()}


class GenderMappingForm(forms.ModelForm):

    class Meta:
        model = GenderMapping
        fields = ('gender', 'local_gender_description','facility')
        widgets = {'facility': forms.HiddenInput()}


class ServiceProviderRankingMappingForm(forms.ModelForm):

    class Meta:
        model = ServiceProviderRankingMapping
        fields = ('service_provider_ranking', 'local_service_provider_ranking_id','local_service_provider_ranking_description','facility')
        widgets = {'facility': forms.HiddenInput()}


class PlaceODeathMappingForm(forms.ModelForm):

    class Meta:
        model = PlaceOfDeathMapping
        fields = ('place_of_death', 'local_place_of_death_id','local_place_of_death_description','facility')
        widgets = {'facility': forms.HiddenInput()}


class CPTCodesMappingForm(forms.ModelForm):

    class Meta:
        model = CPTCodesMapping
        fields = ('cpt_code', 'local_code','facility')
        widgets = {'facility': forms.HiddenInput()}
