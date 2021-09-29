import csv
import json
from ValidationManagement import models as validation_management_models
from django.http import HttpResponse
from .forms import PayloadImportForm, CPTCodeMappingImportForm
from django.shortcuts import render, redirect
from MasterData import models as master_data_models
from django.core.files.storage import FileSystemStorage
from UserManagement import tables as user_management_tables
from django_tables2 import RequestConfig


# Create your views here.
def convert_to_csv(request):
    if request.method == "POST":

        transaction_id = request.POST["item_pk"]
        status = request.POST["status"]

        transaction_lines = validation_management_models.TransactionSummaryLine.objects.filter(transaction_id = transaction_id)
        transaction = validation_management_models.TransactionSummary.objects.get(id=transaction_id)
        message_type = transaction.message_type
        facility_hfr_code = transaction.facility_hfr_code

        instance_facility = master_data_models.Facility.objects.filter(facility_hfr_code = facility_hfr_code).first()
        org_name = instance_facility.description

        model_fields = validation_management_models.TransactionSummaryLine._meta.fields + validation_management_models.TransactionSummaryLine._meta.many_to_many
        field_names = [field.name for field in model_fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.writer(response, delimiter=",")
        fields = []
        # Write a first row with header information

        json_object = transaction_lines.first().payload_object

        if status == "":
            transaction_lines_payload = validation_management_models.TransactionSummaryLine.objects.filter(transaction_id = transaction_id)
        else:
            if status == "fail":
                transaction_lines_payload = validation_management_models.TransactionSummaryLine.objects.filter(transaction_id=transaction_id, transaction_status = 0 )
            else:
                transaction_lines_payload = validation_management_models.TransactionSummaryLine.objects.filter(transaction_id=transaction_id,
                                                                                  transaction_status=1)

        jsonObject = json.loads(json_object)
        fields.append("ID")
        fields.append("TransactionID")
        fields.append("messageType")
        fields.append("facilityHfrCode")
        fields.append("orgName")

        for key in jsonObject:
            fields.append(key)
        writer.writerow(fields)

        for row in transaction_lines_payload:
            json_object = row.payload_object
            values = []
            fields = []
            # for field in field_names:
            jsonObject = json.loads(json_object)

            # Add a column for the message type
            values.append(row.id)
            values.append(transaction_id)
            values.append(message_type)
            values.append(facility_hfr_code)
            values.append(org_name)

            for key in jsonObject:
                value = jsonObject[key]
                fields.append(key)
                if callable(value):
                    try:
                        value = value() or ''
                    except:
                        value = 'Error retrieving value'
                if value is None:
                    value = ''
                values.append(value)
            writer.writerow(values)
        data = response

        return  HttpResponse(data, content_type='text/csv')


def filter_transaction_lines(request):
    if request.method == "POST":
        status = request.POST["status"]
        transaction_id = request.POST["item_pk"]

        if status == "pass":
            transaction_lines = validation_management_models.TransactionSummaryLine.objects.filter(transaction_id = transaction_id, transaction_status = 1)
        else:
            transaction_lines = validation_management_models.TransactionSummaryLine.objects.filter(transaction_id=transaction_id,
                                                                      transaction_status=0)

        transaction_summary_lines_table = user_management_tables.TransactionSummaryLineTable(transaction_lines)
        RequestConfig(request, paginate={"per_page": 10}).configure(transaction_summary_lines_table)

        return render(request,"UserManagement/Dashboard/FilteredElements.html", {"transaction_summary_lines_table":transaction_summary_lines_table})


def download_cpt_codes_as_csv(request):
    queryset = master_data_models.CPTCode.objects.all()
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=CPTCodesMappings.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    field_names.append('local_code')
    # Write a first row with header information
    writer.writerow(field_names)

    field_names.remove('local_code')

    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


def upload_payload(request):
    if request.method == "POST":
        payload_import_form = PayloadImportForm(request.POST, request.FILES)
        if payload_import_form.is_valid():
            payload_import_form.full_clean()
            payload_import_form.save()
        return redirect(request.META['HTTP_REFERER'])


def upload_cpt_codes(request):
    if request.method == "POST":
        cpt_codes_import_form = CPTCodeMappingImportForm(request.POST, request.FILES)
        if cpt_codes_import_form.is_valid():
            cpt_codes_import_form.full_clean()

            file = cpt_codes_import_form.cleaned_data['file']
            instance = master_data_models.Facility.objects.get(id=request.user.profile.facility_id)
            facility_hfr_code = instance.facility_hfr_code
            facility_id = request.user.profile.facility_id

            if not file.name.endswith('.csv'):
                pass
            else:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_path = fs.path(filename)
                save_cpt_code_entries(file_path, facility_id, facility_hfr_code)
        return redirect(request.META['HTTP_REFERER'])


def save_cpt_code_entries(file_path, facility_id, facility_hfr_code):
    # Delete all previous mappings

    instance_previous_mappings = master_data_models.CPTCodesMapping.objects.filter(facility_id=facility_id)
    instance_previous_mappings.delete()

    with open(file_path, 'r') as fp:
        lines = csv.reader(fp, delimiter=',')
        row = 0
        for line in lines:
            if line is not None:
                if row == 0:
                    headers = line
                    row = row + 1
                else:
                    instance_cpt_code_mappings = master_data_models.CPTCodesMapping()
                    instance_cpt_code_mappings.cpt_code_id = line[0]
                    instance_cpt_code_mappings.local_code = line[4]
                    instance_cpt_code_mappings.facility_id = facility_id

                    instance_cpt_code_mappings.save()

            row = row + 1
    fp.close()


def regenerate_services_received_json_payload(request,lines):
    data_items_array = []
    instance = master_data_models.Facility.objects.get(id=request.user.profile.facility_id)
    facility_name = instance.description
    facility_hfr_code = instance.facility_hfr_code

    message_type = ""

    row = 0

    for line in lines:
        message_type = line[2]

        if row > 0:
            json_object = {"deptName": line[5], "deptId": line[6],
                           "patId": line[7],
                           "gender": line[8],
                           "dob": line[9],
                           "medSvcCode": line[10],
                           "icd10Code": line[11],
                           "serviceDate": line[12],
                           "serviceProviderRankingId": line[13],
                           "visitType": line[14]
                           }

            data_items_array.append(json_object)

        row +=1

    parent_object = {
        "messageType": "" + message_type + "",
        "orgName": "" + facility_name + "",
        "facilityHfrCode": "" + facility_hfr_code + "",
        "items": data_items_array
    }

    final_array = json.dumps(parent_object)

    # print(final_array)

    return final_array

