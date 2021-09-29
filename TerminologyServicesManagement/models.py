from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from MasterData import models as master_data_models
import json


# Create your models here.
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

    icd10_code_category = models.ForeignKey(ICD10CodeCategory,related_name='sub_category', on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "ICD10CodeSubCategories"
        verbose_name_plural = "ICD10 Code Sub Categories"


class ICD10Code(models.Model):
    def __str__(self):
        return '%s' %self.icd10_description

    icd10_code_sub_category = models.ForeignKey(ICD10CodeSubCategory,related_name='code', on_delete=models.DO_NOTHING, null=True, blank=True)
    icd10_code = models.CharField(max_length=255)
    icd10_description = models.CharField(max_length=255)

    class Meta:
        db_table="ICD10Codes"
        verbose_name_plural = "ICD10 Codes"


class ICD10SubCode(models.Model):
    def __str__(self):
        return '%d' %self.id

    icd10_code = models.ForeignKey(ICD10Code,related_name='sub_code',on_delete=models.DO_NOTHING, null=True, blank=True)
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

    cpt_code_category = models.ForeignKey(CPTCodeCategory, related_name='sub_category',on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "CPTCodeSubCategories"
        verbose_name_plural = "CPT Code Sub Categories"


class CPTCode(models.Model):
    def __str__(self):
        return '%s' %self.cpt_code

    cpt_code_sub_category = models.ForeignKey(CPTCodeSubCategory,related_name='code', on_delete=models.DO_NOTHING, null=True, blank=True)
    cpt_code = models.CharField(max_length=255)
    cpt_description = models.CharField(max_length=255)

    class Meta:
        db_table = "CPTCodes"
        verbose_name = "CPT Code"


class CPTCodesMapping(models.Model):
    def __str__(self):
        return '%d' % self.id

    cpt_code = models.ForeignKey(CPTCode, on_delete=models.DO_NOTHING, null=True, blank=True)
    local_code = models.CharField(max_length=255)
    facility = models.ForeignKey(master_data_models.Facility, on_delete=models.DO_NOTHING, null=True,
                                 blank=True)

    class Meta:
        db_table = "CPTCodesMappings"


@receiver(post_save, sender=ICD10SubCode)
def send_new_or_updated_icd10_code(sender, instance, created, **kwargs):
    icd10_code_id = instance.icd10_code_id
    icd10_code = ICD10Code.objects.get(id=icd10_code_id)

    icd10_sub_category_id = icd10_code.icd10_code_sub_category_id
    icd10_diagnoses_code = icd10_code.icd10_code
    icd10_description = icd10_code.icd10_description

    icd10_sub_category = ICD10CodeSubCategory.objects.get(id=icd10_sub_category_id)
    icd10_sub_category_description = icd10_sub_category.description

    icd10_category_id = icd10_sub_category.icd10_code_category_id
    icd10_category = ICD10CodeCategory.objects.get(id=icd10_category_id)
    icd10_category_description = icd10_category.description

    object = {
        "icd10_category_description": icd10_category_description,
        "icd10_sub_category_description": icd10_sub_category_description,
        "icd10_code": icd10_diagnoses_code,
        "icd10_description": icd10_description,
        "icd10_sub_code_id":instance.icd10_sub_code,
        "icd10_sub_code_description": instance.icd10_sub_code_description
    }

    json_data = json.dumps(object)

    print(json_data)


    if created:
        pass
        # send new record to emr via him
    else:
        # this is an update
        print("updated instance is", instance)


@receiver(post_save, sender=CPTCode)
def send_new_or_updated_icd10_code(sender, instance, created, **kwargs):
    cpt_code_sub_category_id = instance.cpt_code_sub_category_id
    cpt_code = instance.cpt_code
    cpt_description = instance.cpt_description

    cpt_code_sub_category = CPTCodeSubCategory.objects.get(id=cpt_code_sub_category_id)
    cpt_code_category_id = cpt_code_sub_category.cpt_code_category_id
    cpt_code_sub_category_description  = cpt_code_sub_category.description

    cpt_code_category = CPTCodeCategory.objects.get(id=cpt_code_category_id)
    cpt_code_category_description = cpt_code_category.description

    object = {
        "cpt_code_category_description": cpt_code_category_description,
        "cpt_code_sub_category_description": cpt_code_sub_category_description,
        "cpt_description": cpt_description,
        "cpt_code": cpt_code
    }

    json_data = json.dumps(object)

    print(json_data)

    if created:
        new_cpt_code = instance
        print(new_cpt_code)
        # send new record to emr via him
    else:
        # this is an update
        print("updated instance is", instance)