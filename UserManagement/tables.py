import django_tables2 as tables
from ValidationManagement import models as validation_management_models
from django.utils.safestring import mark_safe
from django.utils.html import escape
import itertools


class Actions(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_audit_report btn btn-success'
                         ' btn-xs"><i class="la la-eye"></i>Audit</button> '
                         '<button id="%s" class="btn_download btn btn-primary'
                         ' btn-xs"><i class="la la-arrow-down"></i>Download</button> '
                         '<button id="%s" class="btn_delete btn btn-danger'
                         ' btn-xs"><i class="la la-trash"></i>Remove</button> '% (escape(record.id), escape(record.id),escape(record.id)))


class TransactionSummaryTable(tables.Table):
    Actions = Actions()
    counter = tables.Column(empty_values=(), orderable=False)
    id = tables.Column(verbose_name='Transaction Id')

    threshold = tables.Column(accessor='threshold', verbose_name='Threshold in (%)')

    total_failed = tables.Column(
        attrs={
            "th": {"id": "total_failed"},
            "td": {"align": "center"}
        }
    )

    total_passed = tables.Column(
        attrs={
            "th": {"id": "total_passed"},
            "td": {"align": "center"}
        }
    )

    class Meta:
        model = validation_management_models.TransactionSummary
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','id','transaction_date_time','message_type','total_passed', 'total_failed','threshold')
        row_attrs = {
            'data-id': lambda record: record.pk,
            "style": lambda record: "background-color:" + record.row_color_codes()
            # "style": lambda record: "background-color: #8B0000;" if record.threshold == 100  else "background-color: #000000;"
        }

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter',
                                   itertools.count(self.page.start_index()))
        return next(self.row_counter)


class TransactionSummaryLineTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False, verbose_name="SN")
    id = tables.Column(verbose_name='Transaction Line ID')
    transaction = tables.Column(verbose_name='Transaction ID')

    class Meta:
        model = validation_management_models.TransactionSummaryLine
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','transaction','id', 'payload_object', 'transaction_status', 'error_message')
        row_attrs = {
            'data-id': lambda record: record.pk
        }

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter',
                                   itertools.count(self.page.start_index()))
        return next(self.row_counter)


class UploadsTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False, verbose_name="SN")

    class Meta:
        model = validation_management_models.PayloadUpload
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','date_time_uploaded','message_type', 'file')
        row_attrs = {
            'data-id': lambda record: record.pk
        }

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter',itertools.count(self.page.start_index()))
        return next(self.row_counter)
