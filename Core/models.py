from django.db import models
from datetime import date
from ValidationManagement import models as validation_management_models

# Create your models here.
def upload_image(self, filename):
    return 'static/payloads/{}'.format(filename)


class ServiceReceived(models.Model):
    def __str__(self):
        return '%d' % self.id

    transaction = models.ForeignKey(validation_management_models.TransactionSummary, on_delete=models.DO_NOTHING, null=True, blank=True)
    org_name = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'ServiceReceived'
        verbose_name_plural = 'Services Received'


class ServiceReceivedItems(models.Model):
    def __str__(self):
        return '%d' % self.id

    service_received = models.ForeignKey(ServiceReceived, on_delete=models.DO_NOTHING, null=True, blank=True)
    department_name = models.CharField(max_length=255)
    department_id = models.CharField(max_length=255)
    patient_id = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    med_svc_code = models.TextField()
    confirmed_diagnosis = models.TextField(null=True, blank=True)
    differential_diagnosis = models.TextField(null=True, blank=True)
    provisional_diagnosis = models.TextField(null=True, blank=True)
    service_date = models.DateField()
    service_provider_ranking_id = models.CharField(max_length=255)
    visit_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'ServiceReceivedItems'
        verbose_name_plural = 'Services Received Items'


class DeathByDiseaseCaseAtFacility(models.Model):
    def __str__(self):
        return '%d' %self.id

    transaction = models.ForeignKey(validation_management_models.TransactionSummary, on_delete=models.DO_NOTHING,
                               null=True, blank=True)
    org_name = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'DeathByDiseaseCaseAtFacility'
        verbose_name_plural = "Death by Disease Cases at Facility"


class DeathByDiseaseCaseAtFacilityItems(models.Model):
    def __str__(self):
        return '%d' % self.id

    death_by_disease_case_at_facility = models.ForeignKey(DeathByDiseaseCaseAtFacility, on_delete=models.DO_NOTHING, null=True, blank=True)
    ward_name = models.CharField(max_length=255)
    ward_id = models.CharField(max_length=255)
    patient_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    cause_of_death = models.CharField(max_length=255)
    immediate_cause_of_death = models.CharField(max_length=255, null=True, blank=True)
    underlying_cause_of_death = models.CharField(max_length=255)
    date_death_occurred = models.CharField(max_length=50)

    class Meta:
        db_table = 'DeathByDiseaseCaseAtFacilityItems'
        verbose_name_plural = "Death by Disease Cases at Facility Items"


class DeathByDiseaseCaseNotAtFacility(models.Model):
    def __str__(self):
        return '%d' %self.id

    transaction = models.ForeignKey(validation_management_models.TransactionSummary, on_delete=models.DO_NOTHING,
                                    null=True, blank=True)
    org_name = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'DeathByDiseaseCaseNotAtFacility'
        verbose_name_plural = "Death by Disease Cases Not at Facility"


class DeathByDiseaseCaseNotAtFacilityItems(models.Model):
    def __str__(self):
        return '%d' %self.id

    death_by_disease_case_not_at_facility = models.ForeignKey(DeathByDiseaseCaseNotAtFacility, on_delete=models.DO_NOTHING, null=True, blank=True)
    place_of_death_id = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    cause_of_death = models.CharField(max_length=255)
    immediate_cause_of_death = models.CharField(max_length=255, null=True, blank=True)
    underlying_cause_of_death = models.CharField(max_length=255, null=True, blank=True)
    date_death_occurred = models.DateField()
    death_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'DeathByDiseaseCaseNotAtFacilityItems'
        verbose_name_plural = "Death by Disease Cases Not at Facility Items"


class BedOccupancy(models.Model):
    def __str__(self):
        return '%d' %self.id

    transaction = models.ForeignKey(validation_management_models.TransactionSummary, on_delete=models.DO_NOTHING,
                                    null=True, blank=True)
    org_name = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'BedOccupancy'
        verbose_name_plural = "Bed occupancy"


class BedOccupancyItems(models.Model):
    def __str__(self):
        return '%d' %self.id

    bed_occupancy = models.ForeignKey(BedOccupancy, on_delete=models.DO_NOTHING, null=True, blank=True)
    patient_id = models.CharField(max_length=255)
    admission_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)
    ward_name = models.CharField(max_length=255)
    ward_id = models.CharField(max_length=255)

    class Meta:
        db_table = 'BedOccupancyItems'
        verbose_name_plural = "Bed occupancy Items"


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

    transaction = models.ForeignKey(validation_management_models.TransactionSummary, on_delete=models.DO_NOTHING,
                                    null=True, blank=True)
    org_name = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'RevenueReceived'
        verbose_name_plural = "Revenue received"


class RevenueReceivedItems(models.Model):
    def __str__(self):
        return '%d' %self.id

    revenue_received = models.ForeignKey(RevenueReceived, on_delete=models.DO_NOTHING, null=True, blank=True)
    system_trans_id = models.CharField(max_length=100)
    transaction_date = models.DateField()
    patient_id = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    med_svc_code = models.TextField()
    payer_id = models.CharField(max_length=50)
    exemption_category_id = models.CharField(max_length=100, null=True, blank=True)
    billed_amount = models.IntegerField(default=0)
    waived_amount = models.IntegerField(default=0)
    service_provider_ranking_id = models.CharField(max_length=255)

    class Meta:
        db_table = 'RevenueReceivedItems'
        verbose_name_plural = "Revenue Received Items"


