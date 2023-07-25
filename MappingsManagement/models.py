from django.db import models
from MasterData import models as master_data_models


# Create your models here.
class PlaceOfDeathMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    place_of_death = models.ForeignKey(master_data_models.PlaceOfDeath, on_delete=models.DO_NOTHING, null=True, blank=True)
    local_place_of_death_id = models.CharField(max_length=255)
    local_place_of_death_description = models.CharField(max_length=255)
    facility = models.ForeignKey(master_data_models.Facility, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        db_table = "PlaceOfDeathMappings"
        verbose_name_plural = "Place of Death Mappings"


class ServiceProviderRankingMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    service_provider_ranking = models.ForeignKey(master_data_models.ServiceProviderRanking, on_delete=models.DO_NOTHING, null=True, blank=True)
    local_service_provider_ranking_id = models.CharField(max_length=255)
    local_service_provider_ranking_description = models.CharField(max_length=255)
    facility = models.ForeignKey(master_data_models.Facility, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        db_table = "ServiceProviderRankingMappings"
        verbose_name_plural = "Service Provider Rankings Mappings"


class GenderMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    gender = models.ForeignKey(master_data_models.Gender, on_delete=models.DO_NOTHING, null=True, blank=True)
    local_gender_description = models.CharField(max_length=50)
    facility = models.ForeignKey(master_data_models.Facility, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        db_table = "GenderMappings"
        verbose_name_plural = "Gender Mappings"


class DepartmentMapping(models.Model):
    def __str__(self):
        return '%d' % self.id

    department = models.ForeignKey(master_data_models.Department, on_delete=models.DO_NOTHING, null=True, blank=True)
    local_department_id = models.CharField(max_length=255)
    local_department_description = models.CharField(max_length=255)
    facility = models.ForeignKey(master_data_models.Facility, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        db_table = "DepartmentMappings"
        verbose_name_plural = "Department Mappings"


class ExemptionMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    exemption = models.ForeignKey(master_data_models.Exemption, on_delete=models.DO_NOTHING, null=True, blank=True)
    local_exemption_id = models.CharField(max_length=255)
    local_exemption_description = models.CharField(max_length=255)
    facility = models.ForeignKey(master_data_models.Facility, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        db_table = "ExemptionMappings"
        verbose_name_plural = "Exemption Mappings"


class PayerMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    payer = models.ForeignKey(master_data_models.Payer, on_delete=models.DO_NOTHING, null=True, blank=True)
    local_payer_id = models.CharField(max_length=255)
    local_payer_description = models.CharField(max_length=255)
    facility = models.ForeignKey(master_data_models.Facility, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        db_table = "PayerMappings"
        verbose_name_plural = "Payer Mappings"