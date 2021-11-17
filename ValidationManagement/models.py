from django.db import models
from MasterData import models as master_data_models


# Create your models here.
class ValidationRule(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)
    rule_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "ValidationRules"


class FieldValidationMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    ServicesReceived = 'SVCREC'
    DeathByDiseaseCaseAtFacility = 'DDC'
    DeathByDiseaseCaseNotAtFacility = 'DDCOUT'
    RevenueReceived = 'REV'
    BedOccupancy = 'BEDOCC'

    MESSAGE_TYPE_CHOICES = (
        (ServicesReceived, 'SVCREC'),
        (DeathByDiseaseCaseAtFacility, 'DDC'),
        (DeathByDiseaseCaseNotAtFacility, 'DDCOUT'),
        (RevenueReceived, 'REV'),
        (BedOccupancy, 'BEDOCC'),
    )

    validation_rule = models.ForeignKey(ValidationRule, on_delete=models.DO_NOTHING, null=True, blank=True)
    message_type = models.CharField(max_length=100, choices=MESSAGE_TYPE_CHOICES)
    field = models.CharField(max_length=255)

    class Meta:
        db_table = "FieldValidationMappings"


class TransactionSummary(models.Model):
    def __str__(self):
        return '%d' %self.id

    def threshold(self):
        return (self.total_passed/(self.total_failed + self.total_passed)) * 100

    def row_color_codes(self):
        message = PayloadThreshold.objects.filter(payload_code=self.message_type).first()
        if message is not None:
            allowed_threshold = message.percentage_threshold
        else:
            allowed_threshold = 0

        total_passed = self.total_passed
        total_failed = self.total_failed

        calculated_threshold = 0

        if total_failed != 0 and total_passed != 0:
            calculated_threshold = self.threshold()
        elif total_passed ==0 and total_failed != 0:
            calculated_threshold = 0
        elif total_passed != 0 and total_failed == 0:
            calculated_threshold = 100

        if calculated_threshold < allowed_threshold:
            row_color = "#F29F41"
        else:
            row_color = "#CDCFB3"

        return row_color

    ServicesReceived = 'SVCREC'
    DeathByDiseaseCaseAtFacility = 'DDC'
    DeathByDiseaseCaseNotAtFacility = 'DDCOUT'
    RevenueReceived = 'REV'
    BedOccupancy = 'BEDOCC'

    MESSAGE_TYPE_CHOICES = (
        (ServicesReceived, 'SVCREC'),
        (DeathByDiseaseCaseAtFacility, 'DDC'),
        (DeathByDiseaseCaseNotAtFacility, 'DDCOUT'),
        (RevenueReceived, 'REV'),
        (BedOccupancy, 'BEDOCC'),
    )

    transaction_date_time = models.DateTimeField(auto_now=True)
    message_type = models.CharField(max_length=100, choices=MESSAGE_TYPE_CHOICES)
    org_name = models.CharField(max_length=255)
    facility_hfr_code  = models.CharField(max_length=255)
    total_passed = models.IntegerField(default=0)
    total_failed = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)


    class Meta:
        db_table = "TransactionSummary"
        verbose_name_plural = "Transactions summary"


class TransactionSummaryLine(models.Model):
    def __str__(self):
        return '%d' %self.id

    transaction = models.ForeignKey(TransactionSummary, on_delete=models.DO_NOTHING, null=True, blank=True)
    payload_object = models.TextField()
    transaction_status = models.BooleanField(default=0)
    error_message = models.TextField()

    class Meta:
        db_table = "TransactionSummaryLine"
        verbose_name_plural = "Transactions summary lines"


class PayloadThreshold(models.Model):
    def __str__(self):
        return '%d' %self.id

    payload_description = models.CharField(max_length=255)
    payload_code = models.CharField(max_length=255)
    percentage_threshold = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "PayloadThreshold"


class PayloadUpload(models.Model):
    def __str__(self):
        return "%d"  % self.id

    ServicesReceived = 'SVCREC'
    DeathByDiseaseCaseAtFacility = 'DDC'
    DeathByDiseaseCaseNotAtFacility = 'DDCOUT'
    RevenueReceived = 'REV'
    BedOccupancy = 'BEDOCC'

    MESSAGE_TYPE_CHOICES = (
        (ServicesReceived, 'SVCREC'),
        (DeathByDiseaseCaseAtFacility, 'DDC'),
        (DeathByDiseaseCaseNotAtFacility, 'DDCOUT'),
        (RevenueReceived, 'REV'),
        (BedOccupancy, 'BEDOCC'),
    )

    date_time_uploaded = models.DateTimeField(auto_now=True)
    message_type = models.CharField(max_length=100, choices=MESSAGE_TYPE_CHOICES)
    file = models.FileField(blank=True, null=True, upload_to="uploads")
    facility = models.ForeignKey(master_data_models.Facility, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "PayloadUploads"