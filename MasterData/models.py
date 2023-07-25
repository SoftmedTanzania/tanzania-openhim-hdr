from django.db import models


# models for mapping
class Zone(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Zones'
        verbose_name_plural = "Zones"


class Region(models.Model):
    def __str__(self):
        return '%s' % self.description

    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Regions'
        verbose_name_plural = "Regions"


class DistrictCouncil(models.Model):
    def __str__(self):
        return '%s' % self.description

    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'DistrictCouncils'
        verbose_name_plural = "District Councils"


class Facility(models.Model):
    def __str__(self):
        return '%s' % self.description

    district_council = models.ForeignKey(DistrictCouncil, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.CharField(max_length=255)
    facility_hfr_code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    uses_cpt_internally = models.BooleanField(default=True)

    class Meta:
        db_table = 'Facility'
        verbose_name_plural = "Facilities"


class Payer(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Payers'
        verbose_name_plural = "Payers"


class Exemption(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "Exemptions"
        verbose_name_plural = "Exemptions"


class Department(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "Departments"
        verbose_name_plural = "Departments"


class Ward(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)
    local_ward_id = models.CharField(max_length=100)
    local_ward_description = models.CharField(max_length=255)
    number_of_beds = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "Wards"
        verbose_name_plural = "Wards"


class Gender(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=50)

    class Meta:
        db_table = "Gender"
        verbose_name_plural = "Gender"


class ServiceProviderRanking(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "ServiceProviderRankings"
        verbose_name_plural = "Service Provider Rankings"


class PlaceOfDeath(models.Model):
    def __str__(self):
        return "%s" %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "PlacesOfDeath"
        verbose_name_plural = "Places Of Death"
