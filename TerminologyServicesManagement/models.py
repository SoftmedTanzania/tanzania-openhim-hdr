from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from MasterData import models as master_data_models
import json
from decouple import config
import requests


him_icd_url = config('HIM_ICD_URL')
him_cpt_url = config('HIM_CPT_URL')

him_username = config('HIM_USERNAME')
him_password = config('HIM_PASSWORD')


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

    category = models.ForeignKey(ICD10CodeCategory,related_name='sub_category', on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "ICD10CodeSubCategories"
        verbose_name_plural = "ICD10 Code Sub Categories"


class ICD10Code(models.Model):
    def __str__(self):
        return '%s' %self.description

    sub_category = models.ForeignKey(ICD10CodeSubCategory,related_name='code', on_delete=models.DO_NOTHING, null=True, blank=True)
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table="ICD10Codes"
        verbose_name_plural = "ICD10 Codes"


class ICD10SubCode(models.Model):
    def __str__(self):
        return '%d' %self.description

    code = models.ForeignKey(ICD10Code,related_name='sub_code',on_delete=models.DO_NOTHING, null=True, blank=True)
    sub_code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table="ICD10SubCodes"
        verbose_name_plural = "ICD10 SubCodes"


class CPTCodeCategory(models.Model):
    def __str__(self):
        return '%d' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table="CPTCodeCategories"
        verbose_name_plural = "CPT Code Categories"


class CPTCodeSubCategory(models.Model):
    def __str__(self):
        return '%d' % self.description

    category = models.ForeignKey(CPTCodeCategory, related_name='sub_category',on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "CPTCodeSubCategories"
        verbose_name_plural = "CPT Code Sub Categories"


class CPTCode(models.Model):
    def __str__(self):
        return '%s' %self.description

    sub_category = models.ForeignKey(CPTCodeSubCategory,related_name='code', on_delete=models.DO_NOTHING, null=True, blank=True)
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

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


# ICD1O Backend events
@receiver(post_save, sender=ICD10CodeCategory)
def send_new_or_updated_icd10_code(sender, instance, created, **kwargs):

    icd10_category_id = instance.id
    icd10_category_description = instance.description

    if created:
        item = {
            "icd10_code_category_id": icd10_category_id,
            "icd10_category_description": icd10_category_description,
            "icd10_sub_category_id": "",
            "icd10_sub_category_description": "",
            "icd10_id": "",
            "icd10_code": "",
            "icd10_description": "",
            "icd10_sub_code_id": "",
            "icd10_sub_code": "",
            "icd10_sub_code_description": "",
            "status": "N"
        }

        json_data = json.dumps(item)

        response = requests.post(him_icd_url,auth=(him_username, him_password),data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})
    else:
        item = {
            "icd10_code_category_id": icd10_category_id,
            "icd10_category_description": icd10_category_description,
            "icd10_sub_category_id": "",
            "icd10_sub_category_description": "",
            "icd10_id": "",
            "icd10_code": "",
            "icd10_description": "",
            "icd10_sub_code_id": "",
            "icd10_sub_code": "",
            "icd10_sub_code_description": "",
            "status": "U"
        }

        json_data = json.dumps(item)

        response = requests.post(him_icd_url, auth=(him_username, him_password),data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})


@receiver(post_save, sender=ICD10CodeSubCategory)
def send_new_or_updated_icd10_code(sender, instance, created, **kwargs):
    icd10_sub_category_id = instance.id
    icd10_sub_category_description = instance.description
    icd10_category_id = instance.category_id

    icd10_category = ICD10CodeCategory.objects.get(id=icd10_category_id)
    icd10_category_description = icd10_category.description

    if created:
        item = {
            "icd10_code_category_id": icd10_category_id,
            "icd10_category_description": icd10_category_description,
            "icd10_sub_category_id": icd10_sub_category_id,
            "icd10_sub_category_description": icd10_sub_category_description,
            "icd10_id": "",
            "icd10_code": "",
            "icd10_description": "",
            "icd10_sub_code_id": "",
            "icd10_sub_code": "",
            "icd10_sub_code_description": "",
            "status": "N"
        }

        json_data = json.dumps(item)

        response = requests.post(him_icd_url,auth=(him_username, him_password),data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})
    else:
        item = {
            "icd10_code_category_id": icd10_category_id,
            "icd10_category_description": icd10_category_description,
            "icd10_sub_category_id": icd10_sub_category_id,
            "icd10_sub_category_description": icd10_sub_category_description,
            "icd10_id": "",
            "icd10_code": "",
            "icd10_description": "",
            "icd10_sub_code_id": "",
            "icd10_sub_code": "",
            "icd10_sub_code_description": "",
            "status": "U"
        }

        json_data = json.dumps(item)

        response = requests.post(him_icd_url, auth=(him_username, him_password),data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})


@receiver(post_save, sender=ICD10Code)
def send_new_or_updated_icd10_code(sender, instance, created, **kwargs):
    icd10_code_id = instance.id
    icd10_code = instance.code
    icd10_code_description = instance.description

    icd10_sub_category = ICD10CodeSubCategory.objects.get(id=instance.sub_category_id)
    icd10_sub_category_id= instance.sub_category_id
    icd10_sub_category_description = icd10_sub_category.description

    icd10_category_id = icd10_sub_category.category_id
    icd10_category = ICD10CodeCategory.objects.get(id=icd10_category_id)
    icd10_category_description = icd10_category.description


    if created:
        item = {
            "icd10_code_category_id": icd10_category_id,
            "icd10_category_description": icd10_category_description,
            "icd10_sub_category_id": str(icd10_sub_category_id),
            "icd10_sub_category_description": icd10_sub_category_description,
            "icd10_id": icd10_code_id,
            "icd10_code": icd10_code,
            "icd10_description": icd10_code_description,
            "icd10_sub_code_id": "",
            "icd10_sub_code": "",
            "icd10_sub_code_description": "",
            "status": "N"
        }

        json_data = json.dumps(item)

        response = requests.post(him_icd_url,auth=(him_username, him_password),data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})
    else:
        item = {
            "icd10_code_category_id": icd10_category_id,
            "icd10_category_description": icd10_category_description,
            "icd10_sub_category_id": str(icd10_sub_category_id),
            "icd10_sub_category_description": icd10_sub_category_description,
            "icd10_id": icd10_code_id,
            "icd10_code": icd10_code,
            "icd10_description": icd10_code_description,
            "icd10_sub_code_id": "",
            "icd10_sub_code": "",
            "icd10_sub_code_description": "",
            "status": "U"
        }

        json_data = json.dumps(item)

        response = requests.post(him_icd_url, auth=(him_username, him_password),data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})


@receiver(post_save, sender=ICD10SubCode)
def send_new_or_updated_icd10_code(sender, instance, created, **kwargs):
    icd10_code_id = instance.code_id
    icd10_code = ICD10Code.objects.get(id=icd10_code_id)

    icd10_sub_category_id = icd10_code.sub_category_id
    icd10_diagnoses_code = icd10_code.code
    icd10_description = icd10_code.description

    icd10_sub_category = ICD10CodeSubCategory.objects.get(id=icd10_sub_category_id)
    icd10_sub_category_description = icd10_sub_category.description

    icd10_category_id = icd10_sub_category.category_id
    icd10_category = ICD10CodeCategory.objects.get(id=icd10_category_id)
    icd10_category_description = icd10_category.description

    if created:
        item = {
            "icd10_code_category_id": icd10_category_id,
            "icd10_category_description": icd10_category_description,
            "icd10_sub_category_id": icd10_sub_category_id,
            "icd10_sub_category_description": icd10_sub_category_description,
            "icd10_id": icd10_code_id,
            "icd10_code": icd10_diagnoses_code,
            "icd10_description": icd10_description,
            "icd10_sub_code_id": instance.id,
            "icd10_sub_code": instance.sub_code,
            "icd10_sub_code_description": instance.description,
            "status": "N"
        }

        json_data = json.dumps(item)

        response = requests.post(him_icd_url,auth=(him_username, him_password),data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})
        print(response)
    else:
        item = {
            "icd10_code_category_id": icd10_category_id,
            "icd10_category_description": icd10_category_description,
            "icd10_sub_category_id": icd10_sub_category_id,
            "icd10_sub_category_description": icd10_sub_category_description,
            "icd10_id": icd10_code_id,
            "icd10_code": icd10_diagnoses_code,
            "icd10_description": icd10_description,
            "icd10_sub_code_id": instance.id,
            "icd10_sub_code": instance.sub_code,
            "icd10_sub_code_description": instance.description,
            "status": "U"
        }

        json_data = json.dumps(item)

        response = requests.post(him_icd_url, auth=(him_username, him_password),data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})


# CPT Backend events
@receiver(post_save, sender=CPTCodeCategory)
def send_new_or_updated_cpt_code(sender, instance, created, **kwargs):
    cpt_code_category_id = instance.id
    cpt_code_category_description = instance.description

    if created:
        item = {
            "cpt_category_code_id": str(cpt_code_category_id),
            "cpt_code_category_description": cpt_code_category_description,
            "cpt_code_sub_category_id": "",
            "cpt_code_sub_category_description": "",
            "cpt_code_id": "",
            "cpt_code": "",
            "cpt_description": "",
            "status": "N"
        }

        json_data = json.dumps(item)

        response = requests.post(him_cpt_url, auth=(him_username, him_password),data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})
    else:
        item = {
            "cpt_category_code_id": str(cpt_code_category_id),
            "cpt_code_category_description": cpt_code_category_description,
            "cpt_code_sub_category_id": "",
            "cpt_code_sub_category_description": "",
            "cpt_code_id": "",
            "cpt_code": "",
            "cpt_description": "",
            "status": "U"
        }

        json_data = json.dumps(item)

        response = requests.post(him_cpt_url, auth=(him_username, him_password), data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})


@receiver(post_save, sender=CPTCodeSubCategory)
def send_new_or_updated_cpt_code(sender, instance, created, **kwargs):
    cpt_code_sub_category_id = instance.id
    cpt_code_sub_category_description = instance.description
    cpt_code_category_id = instance.category_id

    cpt_code_category = CPTCodeCategory.objects.get(id=cpt_code_category_id)
    cpt_code_category_description = cpt_code_category.description

    if created:
        item = {
            "cpt_category_code_id": cpt_code_category_id,
            "cpt_code_category_description": cpt_code_category_description,
            "cpt_code_sub_category_id": cpt_code_sub_category_id,
            "cpt_code_sub_category_description": cpt_code_sub_category_description,
            "cpt_code_id": "",
            "cpt_code": "",
            "cpt_description": "",
            "status": "N"
        }

        json_data = json.dumps(item)

        response = requests.post(him_cpt_url, auth=(him_username, him_password), data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})
    else:
        item = {
            "cpt_category_code_id": cpt_code_category_id,
            "cpt_code_category_description": cpt_code_category_description,
            "cpt_code_sub_category_id": cpt_code_sub_category_id,
            "cpt_code_sub_category_description": cpt_code_sub_category_description,
            "cpt_code_id": "",
            "cpt_code": "",
            "cpt_description": "",
            "status": "U"
        }

        json_data = json.dumps(item)

        response = requests.post(him_cpt_url, auth=(him_username, him_password), data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})


@receiver(post_save, sender=CPTCode)
def send_new_or_updated_cpt_code(sender, instance, created, **kwargs):
    cpt_code_sub_category_id = instance.sub_category_id
    cpt_code = instance.code
    cpt_description = instance.description

    cpt_code_sub_category = CPTCodeSubCategory.objects.get(id=cpt_code_sub_category_id)
    cpt_code_category_id = cpt_code_sub_category.category_id
    cpt_code_sub_category_description  = cpt_code_sub_category.description

    cpt_code_category = CPTCodeCategory.objects.get(id=cpt_code_category_id)
    cpt_code_category_description = cpt_code_category.description

    if created:
        item = {
            "cpt_category_code_id": cpt_code_category_id,
            "cpt_code_category_description": cpt_code_category_description,
            "cpt_code_sub_category_id": cpt_code_sub_category_id,
            "cpt_code_sub_category_description": cpt_code_sub_category_description,
            "cpt_code_id": instance.id,
            "cpt_code": cpt_code,
            "cpt_description": cpt_description,
            "status": "N"
        }

        json_data = json.dumps(item)

        response = requests.post(him_cpt_url, auth=(him_username, him_password),data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})
    else:
        item = {
            "cpt_category_code_id": cpt_code_category_id,
            "cpt_code_category_description": cpt_code_category_description,
            "cpt_code_sub_category_id": cpt_code_sub_category_id,
            "cpt_code_sub_category_description": cpt_code_sub_category_description,
            "cpt_code_id": instance.id,
            "cpt_code": cpt_code,
            "cpt_description": cpt_description,
            "status": "U"
        }

        json_data = json.dumps(item)

        response = requests.post(him_cpt_url, auth=(him_username, him_password), data=json_data,
                                 headers={'User-Agent': 'XY', 'Content-type': 'application/json'})