from django.db import models


# models for mapping
class Zone(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Zones'


class Region(models.Model):
    def __str__(self):
        return '%s' % self.description

    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Regions'


class DistrictCouncil(models.Model):
    def __str__(self):
        return '%s' % self.description

    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'DistrictCouncils'


class Facility(models.Model):
    def __str__(self):
        return '%s' % self.description

    district_council = models.ForeignKey(DistrictCouncil, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = 'facility'
        verbose_name_plural = "Facilities"


class Payer(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Payers'


class PayerMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    payer = models.ForeignKey(Payer, on_delete=models.CASCADE, null=True, blank=True)
    local_payer_id = models.CharField(max_length=255)
    local_payer_description = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "PayerMappings"


class Exemption(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "Exemptions"


class ExemptionMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    exemption = models.ForeignKey(Exemption, on_delete=models.CASCADE, null=True, blank=True)
    local_exemption_id = models.CharField(max_length=255)
    local_exemption_description = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "ExemptionMappings"


class Department(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "Departments"


class DepartmentMapping(models.Model):
    def __str__(self):
        return '%d' % self.id

    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    local_department_id = models.CharField(max_length=255)
    local_department_description = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "DepartmentMappings"


class Ward(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)
    local_ward_id = models.CharField(max_length=100)
    local_ward_description = models.CharField(max_length=255)
    number_of_beds = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "Wards"


class Gender(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=50)

    class Meta:
        db_table = "Gender"


class GenderMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    local_gender_description = models.CharField(max_length=50)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "GenderMappings"


class ICD10CodeCategory(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table="ICD10CodeCategories"
        verbose_name_plural = "ICD10 Code Categories"


class ICD10CodeSubCategory(models.Model):
    def __str__(self):
        return '%s' % self.description

    icd_10_code_category = models.ForeignKey(ICD10CodeCategory, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "ICD10CodeSubCategories"
        verbose_name_plural = "ICD10 Code Sub Categories"


class ICD10Code(models.Model):
    def __str__(self):
        return '%s' %self.icd10_description

    icd_10_code_sub_category = models.ForeignKey(ICD10CodeSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    icd10_code = models.CharField(max_length=255)
    icd10_description = models.CharField(max_length=255)

    class Meta:
        db_table="ICD10Codes"
        verbose_name_plural = "ICD10 Codes"

class ICD10SubCode(models.Model):
    def __str__(self):
        return '%d' %self.id

    icd10_code = models.ForeignKey(ICD10Code, on_delete=models.CASCADE, null=True, blank=True)
    icd10_sub_code = models.CharField(max_length=255)
    icd10_sub_code_description = models.CharField(max_length=255)

    class Meta:
        db_table="ICD10SubCodes"
        verbose_name_plural = "ICD10 SubCodes"


class CPTCodeCategory(models.Model):
    def __str__(self):
        return '%d' %self.id

    description = models.CharField(max_length=255)

    class Meta:
        db_table="CPTCodeCategories"
        verbose_name_plural = "CPT Code Categories"


class CPTCodeSubCategory(models.Model):
    def __str__(self):
        return '%d' % self.id

    cpt_code_category = models.ForeignKey(CPTCodeCategory, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "CPTCodeSubCategories"
        verbose_name_plural = "CPT Code Sub Categories"


class CPTCode(models.Model):
    def __str__(self):
        return '%s' %self.cpt_code

    cpt_code_sub_category = models.ForeignKey(CPTCodeSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    cpt_code = models.CharField(max_length=255)
    cpt_description = models.CharField(max_length=255)

    class Meta:
        db_table = "CPTCodes"


class ServiceProviderRanking(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "ServiceProviderRankings"


class ServiceProviderRankingMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    service_provider_ranking = models.ForeignKey(ServiceProviderRanking, on_delete=models.CASCADE, null=True, blank=True)
    local_service_provider_ranking_id = models.CharField(max_length=255)
    local_service_provider_ranking_description = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "ServiceProviderRankingMappings"


class PlaceOfDeath(models.Model):
    def __str__(self):
        return "%s" %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "PlacesOfDeath"
        verbose_name_plural = "Places Of Death"


class PlaceOfDeathMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    place_of_death = models.ForeignKey(PlaceOfDeath, on_delete=models.CASCADE, null=True, blank=True)
    local_place_of_death_id = models.CharField(max_length=255)
    local_place_of_death_description = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "PlaceOfDeathMappings"


class CPTCodesMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    cpt_code = models.ForeignKey(CPTCode, on_delete=models.CASCADE, null=True, blank=True)
    local_code = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "CPTCodesMappings"
