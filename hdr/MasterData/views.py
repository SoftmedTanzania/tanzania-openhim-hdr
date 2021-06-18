from django.shortcuts import render, redirect, HttpResponse
from .tables import PayerMappingTable, ExemptionMappingTable, DepartmentMappingTable, WardMappingTable, \
    GenderMappingTable, ServiceProviderRankingMappingTable, PlaceODeathMappingTable, CPTCodeMappingTable
from .models import PayerMapping, DepartmentMapping, ExemptionMapping, Ward,CPTCodesMapping, GenderMapping, \
    ServiceProviderRankingMapping, PlaceOfDeathMapping, ICD10CodeCategory, ICD10CodeSubCategory, ICD10Code, ICD10SubCode,CPTCode
from .forms import DepartmentMappingForm, ExemptionMappingForm, PayerMappingForm, WardMappingForm, GenderMappingForm, \
    ServiceProviderRankingMappingForm, PlaceODeathMappingForm, CPTCodesMappingForm
from django_tables2 import RequestConfig
from Core import forms as core_forms
import json


def get_departments_page(request):
    if request.method == "POST":
        department_mapping_form = DepartmentMappingForm(request.POST)

        if department_mapping_form.is_valid():
            department_mapping_form.full_clean()
            department_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        department_mappings = DepartmentMapping.objects.filter(facility=facility)
        department_mappings_table = DepartmentMappingTable(department_mappings)
        department_mapping_form = DepartmentMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(department_mappings_table)
        return render(request, 'MasterData/Features/Departments.html',{"department_mappings_table": department_mappings_table,
                                                                       "department_mapping_form" : department_mapping_form})


def update_department(request, item_pk):
    instance_department = DepartmentMapping.objects.get(id=item_pk)
    form = DepartmentMappingForm(instance=instance_department)

    if request.method == "POST":
        if request.POST:
            form_department = DepartmentMappingForm(request.POST, instance=instance_department)
            if form_department.is_valid():
                form_department.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Department"
        url = "update_department"

        return render(request, 'MasterData/Features/UpdateItem.html', {'form': form, 'header': header,
                                                                       'item_pk':item_pk, "url":url
                                                                       })
    return redirect(request.META['HTTP_REFERER'])


def get_cpt_codes_page(request):
    if request.method == "POST":
        cpt_codes_mapping_form = CPTCodesMappingForm(request.POST)

        if cpt_codes_mapping_form.is_valid():
            cpt_codes_mapping_form.full_clean()
            cpt_codes_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        cpt_code_mappings = CPTCodesMapping.objects.filter(facility=facility)
        cpt_code_mappings_table = CPTCodeMappingTable(cpt_code_mappings)
        cpt_code_mapping_form = CPTCodesMappingForm(initial={'facility': request.user.profile.facility})
        cpt_code_mapping_import_form = core_forms.CPTCodeMappingImportForm()
        RequestConfig(request, paginate={"per_page": 10}).configure(cpt_code_mappings_table)
        return render(request, 'MasterData/Features/CPTCodes.html',
                      {"cpt_code_mappings_table": cpt_code_mappings_table,
                       "cpt_code_mapping_form": cpt_code_mapping_form,
                       "cpt_code_mapping_import_form":cpt_code_mapping_import_form})


def update_cpt_code(request, item_pk):
    instance_cpt_code = CPTCodesMapping.objects.get(id=item_pk)
    form = CPTCodesMappingForm(instance=instance_cpt_code)

    if request.method == "POST":
        if request.POST:
            form_cpt_code = CPTCodesMappingForm(request.POST, instance=instance_cpt_code)
            if form_cpt_code.is_valid():
                form_cpt_code.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update CPT code"
        url = "update_cpt_code"

        return render(request, 'MasterData/Features/UpdateItem.html', {'form': form, 'header': header,
                                                                       'item_pk': item_pk, "url": url
                                                                       })
    return redirect(request.META['HTTP_REFERER'])


def get_exemptions_page(request):
    if request.method == "POST":
        exemption_mapping_form = ExemptionMappingForm(request.POST)

        if exemption_mapping_form.is_valid():
            exemption_mapping_form.full_clean()
            exemption_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        exemption_mappings = ExemptionMapping.objects.filter(facility=facility)
        exemption_mappings_table = ExemptionMappingTable(exemption_mappings)
        exemption_mapping_form = ExemptionMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(exemption_mappings_table)
        return render(request, 'MasterData/Features/Exemptions.html',{"exemption_mappings_table":exemption_mappings_table,
                                                                      "exemption_mapping_form":exemption_mapping_form})


def update_exemption(request, item_pk):
    instance_exemption = ExemptionMapping.objects.get(id=item_pk)
    form = ExemptionMappingForm(instance=instance_exemption)

    if request.method == "POST":
        if request.POST:
            form_exemption = ExemptionMappingForm(request.POST, instance=instance_exemption)
            if form_exemption.is_valid():
                form_exemption.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Exemption"
        url = "update_exemption"

        return render(request, 'MasterData/Features/UpdateItem.html', {'form': form, 'header': header,
                                                                       'item_pk':item_pk, "url":url
                                                                       })
    return redirect(request.META['HTTP_REFERER'])


def get_payers_page(request):
    if request.method == "POST":
        payer_mapping_form = PayerMappingForm(request.POST)

        if payer_mapping_form.is_valid():
            payer_mapping_form.full_clean()
            payer_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        payer_mappings = PayerMapping.objects.filter(facility=facility)
        payer_mappings_table = PayerMappingTable(payer_mappings)
        payer_mapping_form = PayerMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(payer_mappings_table)
        return render(request, 'MasterData/Features/Payers.html', {"payer_mappings_table":payer_mappings_table,
                                                                   "payer_mapping_form":payer_mapping_form})


def update_payer(request, item_pk):
    instance_payer = PayerMapping.objects.get(id=item_pk)
    form = PayerMappingForm(instance=instance_payer)

    if request.method == "POST":
        if request.POST:
            form_payer = PayerMappingForm(request.POST, instance=instance_payer)
            if form_payer.is_valid():
                form_payer.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Payer"
        url = "update_payer"

        return render(request, 'MasterData/Features/UpdateItem.html', {'form': form, 'header': header,
                                                                       'item_pk':item_pk, "url":url
                                                                       })
    return redirect(request.META['HTTP_REFERER'])


def get_wards_page(request):
    if request.method == "POST":
        ward_mapping_form = WardMappingForm(request.POST)

        if ward_mapping_form.is_valid():
            ward_mapping_form.full_clean()
            ward_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        ward_mappings = Ward.objects.filter(facility=facility)
        ward_mappings_table = WardMappingTable(ward_mappings)
        ward_mapping_form = WardMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(ward_mappings_table)
        return render(request, 'MasterData/Features/Wards.html',{"ward_mappings_table":ward_mappings_table,
                                                                 "ward_mapping_form":ward_mapping_form})


def update_ward(request, item_pk):
    instance_ward = Ward.objects.get(id=item_pk)
    form = WardMappingForm(instance=instance_ward)

    if request.method == "POST":
        if request.POST:
            form_ward = WardMappingForm(request.POST, instance=instance_ward)
            if form_ward.is_valid():
                form_ward.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Ward"
        url = "update_ward"

        return render(request, 'MasterData/Features/UpdateItem.html', {'form': form, 'header': header,
                                                                       'item_pk':item_pk, "url":url
                                                                       })
    return redirect(request.META['HTTP_REFERER'])


def get_gender_page(request):
    if request.method == "POST":
        gender_mapping_form = GenderMappingForm(request.POST)

        if gender_mapping_form.is_valid():
            gender_mapping_form.full_clean()
            gender_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        gender_mappings = GenderMapping.objects.filter(facility=facility)
        gender_mappings_table = GenderMappingTable(gender_mappings)
        gender_mapping_form = GenderMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(gender_mappings_table)
        return render(request, 'MasterData/Features/Gender.html', {"gender_mappings_table": gender_mappings_table,
                                                                   "gender_mapping_form": gender_mapping_form})


def update_gender(request, item_pk):
    instance_gender = GenderMapping.objects.get(id=item_pk)
    form = GenderMappingForm(instance=instance_gender)

    if request.method == "POST":
        if request.POST:
            form_gender = GenderMappingForm(request.POST, instance=instance_gender)
            if form_gender.is_valid():
                form_gender.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Gender"
        url = "update_gender"

        return render(request, 'MasterData/Features/UpdateItem.html', {'form': form, 'header': header,
                                                                       'item_pk':item_pk, "url":url
                                                                       })
    return redirect(request.META['HTTP_REFERER'])


def get_service_provider_rankings_page(request):
    if request.method == "POST":
        service_provider_ranking_mapping_form = ServiceProviderRankingMappingForm(request.POST)

        if service_provider_ranking_mapping_form.is_valid():
            service_provider_ranking_mapping_form.full_clean()
            service_provider_ranking_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        service_provider_ranking_mappings = ServiceProviderRankingMapping.objects.filter(facility=facility)
        service_provider_ranking_mappings_table = ServiceProviderRankingMappingTable(service_provider_ranking_mappings)
        service_provider_ranking_mapping_mapping_form = ServiceProviderRankingMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(service_provider_ranking_mappings_table)
        return render(request, 'MasterData/Features/ServiceProviderRankings.html',
                      {"service_provider_ranking_mappings_table": service_provider_ranking_mappings_table,
                       "service_provider_ranking_mappings_form": service_provider_ranking_mapping_mapping_form})


def update_service_provider_ranking(request, item_pk):
    instance_server_provider_ranking = ServiceProviderRankingMapping.objects.get(id=item_pk)
    form = ServiceProviderRankingMappingForm(instance=instance_server_provider_ranking)

    if request.method == "POST":
        if request.POST:
            form_service_provider_ranking = ServiceProviderRankingMappingForm(request.POST, instance=instance_server_provider_ranking)
            if form_service_provider_ranking.is_valid():
                form_service_provider_ranking.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Service Provider Ranking"
        url = "update_service_provider_ranking"

        return render(request, 'MasterData/Features/UpdateItem.html', {'form': form, 'header': header,
                                                                       'item_pk': item_pk, "url": url
                                                                       })
    return redirect(request.META['HTTP_REFERER'])


def get_places_of_death_page(request):
    if request.method == "POST":
        place_of_death_mapping_form = PlaceODeathMappingForm(request.POST)

        if place_of_death_mapping_form.is_valid():
            place_of_death_mapping_form.full_clean()
            place_of_death_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        place_of_death_mappings = PlaceOfDeathMapping.objects.filter(facility=facility)
        place_of_death_mappings_table = PlaceODeathMappingTable(place_of_death_mappings)
        place_of_death_mapping_form = PlaceODeathMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(place_of_death_mappings_table)
        return render(request, 'MasterData/Features/PlacesOfDeath.html',
                      {"place_of_death_mappings_table": place_of_death_mappings_table,
                       "place_of_death_mapping_form": place_of_death_mapping_form})


def update_place_of_death(request, item_pk):
    instance_place_of_death = ServiceProviderRankingMapping.objects.get(id=item_pk)
    form = ServiceProviderRankingMappingForm(instance=instance_place_of_death)

    if request.method == "POST":
        if request.POST:
            form_place_of_death = PlaceODeathMappingForm(request.POST,instance=instance_place_of_death)
            if form_place_of_death.is_valid():
                form_place_of_death.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Place Of Death"
        url = "update_place_of_death"

        return render(request, 'MasterData/Features/UpdateItem.html', {'form': form, 'header': header,
                                                                       'item_pk': item_pk, "url": url
                                                                       })
    return redirect(request.META['HTTP_REFERER'])


def delete_mapping(request):
    if request.method == "POST":
        mapping_id = int(request.POST["mapping_id"])
        mapping_type = request.POST["mapping_type"]

        if mapping_type == "departments":
            DepartmentMapping.objects.get(id=mapping_id).delete()
        elif mapping_type == "exemptions":
            ExemptionMapping.objects.get(id=mapping_id).delete()
        elif mapping_type == "payers":
            PayerMapping.objects.get(id=mapping_id).delete()
        elif mapping_type == "wards":
            Ward.objects.get(id=mapping_id).delete()
        elif mapping_type == "gender":
            GenderMapping.objects.get(id=mapping_id).delete()
        elif mapping_type == "places_of_death":
            PlaceOfDeathMapping.objects.get(id=mapping_id).delete()
        elif mapping_type == "rankings":
            ServiceProviderRankingMapping.objects.get(id=mapping_id).delete()
        elif mapping_type == "cpt_codes_mappings":
            CPTCodesMapping.objects.get(id=mapping_id).delete()

    return redirect(request.META['HTTP_REFERER'])


def import_icd_10_codes(request):
    with open ('icd10codes.json',"r") as f:
        data = json.load(f)

    for x in data:
        categories = x['category']
        sub_categories = x['subCategories']

        # # insert category
        instance_category = ICD10CodeCategory()
        instance_category.description = categories
        instance_category.save()

        for sub_category in sub_categories:
            sub_category_name = sub_category['subCategoryName']
            sub_sub_categories = sub_category['subSubCategories']

            # # insert sub category
            instance_sub_category = ICD10CodeSubCategory()
            instance_sub_category.description = sub_category_name
            instance_sub_category.icd_10_code_category_id = instance_category.id
            instance_sub_category.save()

            # loop through the sub sub categories
            for sub_sub_category in sub_sub_categories:
                icd_10 = sub_sub_category["subSubCategoryName"]
                icd_10_code = sub_sub_category["subSubCategoryCode"]
                icd_sub_code_array = sub_sub_category["icd10Codes"]

                # # insert icd code
                instance_icd_code = ICD10Code()
                instance_icd_code.icd_10_code_sub_category_id =  instance_sub_category.id
                instance_icd_code.icd10_code = icd_10_code
                instance_icd_code.icd10_description = icd_10
                instance_icd_code.save()

                for y in icd_sub_code_array:
                    icd_10_sub_code = y["icd10Code"]
                    icd_10_sub_description = y["icd10Name"]

                    # # insert icd sub code
                    instance_icd_sub_code = ICD10SubCode()
                    instance_icd_sub_code.icd10_code_id = instance_icd_code.id
                    instance_icd_sub_code.icd10_sub_code = icd_10_sub_code
                    instance_icd_sub_code.icd10_sub_code_description = icd_10_sub_description
                    instance_icd_sub_code.save()

                return HttpResponse("Finished Uploading")




