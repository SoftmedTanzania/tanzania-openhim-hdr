import django_tables2 as tables
from MasterData import models as master_data_models
from django.utils.safestring import mark_safe
from django.utils.html import escape
import itertools


class Actions(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_delete btn btn-danger'
                         ' btn-sm"><i class="la la-trash"></i>Delete</button> '
                         '<button id="%s" class="btn_update btn btn-primary'
                         ' btn-sm"><i class="la la-pencil"></i>Edit</button> '
                         %  (escape(record.id),escape(record.id)))


class PayerMappingTable(tables.Table):
    Actions = Actions()
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = master_data_models.PayerMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','payer','local_payer_id','local_payer_description' )
        row_attrs = {
            'data-id': lambda record: record.pk
        }

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter',
                                   itertools.count(self.page.start_index()))
        return next(self.row_counter)


class ExemptionMappingTable(tables.Table):
    Actions = Actions()
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = master_data_models.ExemptionMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','exemption','local_exemption_id','local_exemption_description' )
        row_attrs = {
            'data-id': lambda record: record.pk
        }

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter',
                                   itertools.count(self.page.start_index()))
        return next(self.row_counter)

class DepartmentMappingTable(tables.Table):
    Actions = Actions()
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = master_data_models.DepartmentMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','department','local_department_id','local_department_description' )
        row_attrs = {
            'data-id': lambda record: record.pk
        }

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter',
                                   itertools.count(self.page.start_index()))
        return next(self.row_counter)


class WardMappingTable(tables.Table):
    Actions = Actions()
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = master_data_models.Ward
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','description','local_ward_id','local_ward_description', 'number_of_beds','department' )
        row_attrs = {
            'data-id': lambda record: record.pk
        }

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter',
                                   itertools.count(self.page.start_index()))
        return next(self.row_counter)


class GenderMappingTable(tables.Table):
    Actions = Actions()
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = master_data_models.GenderMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','gender','local_gender_description' )
        row_attrs = {
            'data-id': lambda record: record.pk
        }

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter',
                                   itertools.count(self.page.start_index()))
        return next(self.row_counter)

class ServiceProviderRankingMappingTable(tables.Table):
    Actions = Actions()
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = master_data_models.ServiceProviderRankingMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','service_provider_ranking', 'local_service_provider_ranking_id','local_service_provider_ranking_description')
        row_attrs = {
            'data-id': lambda record: record.pk
        }

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter',
                                   itertools.count(self.page.start_index()))
        return next(self.row_counter)

class PlaceODeathMappingTable(tables.Table):
    Actions = Actions()
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = master_data_models.PlaceOfDeathMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','place_of_death', 'local_place_of_death_id','local_place_of_death_description')
        row_attrs = {
            'data-id': lambda record: record.pk
        }

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter',
                                   itertools.count(self.page.start_index()))
        return next(self.row_counter)


class CPTCodeMappingTable(tables.Table):
    Actions = Actions()
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = master_data_models.CPTCodesMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','cpt_code', 'cpt_code__cpt_description','local_code')
        row_attrs = {
            'data-id': lambda record: record.pk
        }

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter',
                                   itertools.count(self.page.start_index()))
        return next(self.row_counter)
