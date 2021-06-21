from django.db import models
from datetime import date

# Create your models here.
def upload_image(self, filename):
    return 'static/payloads/{}'.format(filename)


class ServiceReceived(models.Model):
    def __str__(self):
        return '%d' %self.id

    org_name = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'ServiceReceived'
        verbose_name_plural = 'Services Received'


class ServiceReceivedItems(models.Model):
    def __str__(self):
        return '%d' % self.id

    service_received = models.ForeignKey(ServiceReceived, on_delete=models.CASCADE, null=True, blank=True)
    department_name = models.CharField(max_length=255)
    department_id = models.CharField(max_length=255)
    patient_id = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    med_svc_code = models.CharField(max_length=255)
    icd_10_code = models.CharField(max_length=255, null=True, blank=True)
    service_date = models.DateField()
    service_provider_ranking_id = models.CharField(max_length=255)
    visit_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'ServiceReceivedItems'
        verbose_name_plural = 'Services Received Items'


class DeathByDiseaseCaseAtFacility(models.Model):
    def __str__(self):
        return '%d' %self.id

    org_name = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'DeathByDiseaseCaseAtFacility'
        verbose_name_plural = "Death by Disease Cases at Facility"


class DeathByDiseaseCaseAtFacilityItems(models.Model):
    def __str__(self):
        return '%d' % self.id

    death_by_disease_case_at_facility = models.ForeignKey(DeathByDiseaseCaseAtFacility, on_delete=models.CASCADE, null=True, blank=True)
    ward_name = models.CharField(max_length=255)
    ward_id = models.CharField(max_length=255)
    patient_id = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    icd_10_code = models.CharField(max_length=255, null=True, blank=True)
    date_death_occurred = models.DateField()

    class Meta:
        db_table = 'DeathByDiseaseCaseAtFacilityItems'
        verbose_name_plural = "Death by Disease Cases at Facility Items"


class DeathByDiseaseCaseNotAtFacility(models.Model):
    def __str__(self):
        return '%d' %self.id

    org_name = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'DeathByDiseaseCaseNotAtFacility'
        verbose_name_plural = "Death by Disease Cases Not at Facility"


class DeathByDiseaseCaseNotAtFacilityItems(models.Model):
    def __str__(self):
        return '%d' %self.id

    death_by_disease_case_not_at_facility = models.ForeignKey(DeathByDiseaseCaseNotAtFacility, on_delete=models.CASCADE, null=True, blank=True)
    place_of_death_id = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    icd_10_code = models.CharField(max_length=255, null=True, blank=True)
    date_death_occurred = models.DateField()
    death_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'DeathByDiseaseCaseNotAtFacilityItems'
        verbose_name_plural = "Death by Disease Cases Not at Facility Items"


class BedOccupancy(models.Model):
    def __str__(self):
        return '%d' %self.id

    org_name = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'BedOccupancy'
        verbose_name_plural = "Bed occupancy"


class BedOccupancyItems(models.Model):
    def __str__(self):
        return '%d' %self.id

    bed_occupancy = models.ForeignKey(BedOccupancy, on_delete=models.CASCADE, null=True, blank=True)
    patient_id = models.CharField(max_length=255)
    admission_date = models.DateField()
    discharge_date = models.DateField()
    ward_name = models.CharField(max_length=255)
    ward_id = models.CharField(max_length=255)

    class Meta:
        db_table = 'BedOccupancyItems'
        verbose_name_plural = "Bed occupancyItems"


class BedOccupancyReport(models.Model):
    def __str__(self):
        return '%d' % self.id

    patient_id = models.CharField(max_length=100)
    ward_id = models.CharField(max_length=100)
    ward_name = models.CharField(max_length=255)
    admission_date = models.DateField(default=date.today)
    date = models.DateField()
    bed_occupancy = models.DecimalField(decimal_places=4, max_digits=7)
    facility_hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = "BedOccupancyReport"


class RevenueReceived(models.Model):
    def __str__(self):
        return '%d' %self.id

    org_name = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'RevenueReceived'
        verbose_name_plural = "Revenue received"


class RevenueReceivedItems(models.Model):
    def __str__(self):
        return '%d' %self.id

    revenue_received = models.ForeignKey(RevenueReceived, on_delete=models.CASCADE, null=True, blank=True)
    system_trans_id = models.CharField(max_length=100)
    transaction_date = models.DateField()
    patient_id = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    med_svc_code = models.CharField(max_length=50)
    payer_id = models.CharField(max_length=50)
    exemption_category_id = models.CharField(max_length=100, null=True, blank=True)
    billed_amount = models.IntegerField(default=0)
    waived_amount = models.IntegerField(default=0)
    service_provider_ranking_id = models.CharField(max_length=255)

    class Meta:
        db_table = 'RevenueReceivedItems'
        verbose_name_plural = "Revenue Received Items"


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

    validation_rule = models.ForeignKey(ValidationRule, on_delete=models.CASCADE, null=True, blank=True)
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


    class Meta:
        db_table = "TransactionSummary"
        verbose_name_plural = "Transactions summary"


class TransactionSummaryLine(models.Model):
    def __str__(self):
        return '%d' %self.id

    transaction = models.ForeignKey(TransactionSummary, on_delete=models.CASCADE, null=True, blank=True)
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

    class Meta:
        db_table = "PayloadUploads"


