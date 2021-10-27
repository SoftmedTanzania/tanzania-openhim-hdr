import csv
import json
from celery import Celery
from API import validators as validators
from Core import models as core_models
from MasterData import models as master_data_models
import os
from django.http import HttpResponse
from datetime import datetime, timedelta
from pathlib import Path
from Core import views as core_views
from ValidationManagement import models as validation_management_models

app = Celery()


@app.task()
def save_payload_from_csv():
    print("function was called")
    root_path = "uploads"
    i = 0
    for subdir, _, _ in os.walk(root_path):
        print("subdir was called")
        for file in os.listdir(subdir):
            print("function was called")
            file_path = "" + root_path + "/" + file
            with open(file_path, 'r') as fp:
                print("open file path was called")
                lines = csv.reader(fp, delimiter=',')

                imported_payload = core_views.regenerate_json_payload_from_csv(lines)

                result = validators.validate_received_payload(json.loads(imported_payload))
                transaction_status = result["transaction_status"]
                transaction_id = result["transaction_id"]

                os.remove(file_path)
                fp.close()

                if transaction_status is False:
                    print("validation failed")
                else:
                    print("validation successful")
                    json_imported_payload = json.loads(imported_payload)
                    print(json_imported_payload)
                    message_type = json_imported_payload["messageType"]
                    facility_name = json_imported_payload["orgName"]
                    facility_hfr_code = json_imported_payload["facilityHfrCode"]

                    items = json_imported_payload["items"]

                    # Service received parents lines
                    if message_type == "SVCREC":
                        instance_service_received = core_models.ServiceReceived()
                        instance_service_received.transaction_id = transaction_id
                        instance_service_received.org_name = facility_name
                        instance_service_received.facility_hfr_code = facility_hfr_code
                        instance_service_received.save()

                        for item in items:
                            instance_service_received_items = core_models.ServiceReceivedItems()
                            instance_service_received_items.service_received_id = instance_service_received.id
                            instance_service_received_items.department_name = item["deptName"]
                            instance_service_received_items.department_id = item["deptId"]
                            instance_service_received_items.patient_id = item["patId"]
                            instance_service_received_items.gender = item["gender"]
                            instance_service_received_items.date_of_birth = validators.convert_date_formats(item["dob"])
                            instance_service_received_items.med_svc_code = item["medSvcCode"]
                            instance_service_received_items.icd_10_code = item["icd10Code"]
                            instance_service_received_items.service_date = validators.convert_date_formats(item["serviceDate"])
                            instance_service_received_items.service_provider_ranking_id = item["serviceProviderRankingId"]
                            instance_service_received_items.visit_type = item["visitType"]
                            instance_service_received_items.save()

                    # Death in Facility
                    if message_type == "DDC":
                        instance_death_by_disease_case_at_facility = core_models.DeathByDiseaseCaseAtFacility()
                        instance_death_by_disease_case_at_facility.transaction_id = transaction_id
                        instance_death_by_disease_case_at_facility.org_name = facility_name
                        instance_death_by_disease_case_at_facility.facility_hfr_code = facility_hfr_code
                        instance_death_by_disease_case_at_facility.save()

                        for item in items:
                            instance_death_by_disease_case_items = core_models.DeathByDiseaseCaseAtFacility()
                            instance_death_by_disease_case_items.death_by_disease_case_at_facility_id = instance_death_by_disease_case_at_facility.id
                            instance_death_by_disease_case_items.ward_id = item["wardId"]
                            instance_death_by_disease_case_items.ward_name = item["wardName"]
                            instance_death_by_disease_case_items.patient_id = item["patId"]
                            instance_death_by_disease_case_items.first_name = item["firstName"]
                            instance_death_by_disease_case_items.middle_name = item["middleName"]
                            instance_death_by_disease_case_items.last_name = item["lastName"]
                            instance_death_by_disease_case_items.gender = item["gender"]
                            instance_death_by_disease_case_items.date_of_birth = item["dob"]
                            instance_death_by_disease_case_items.icd_10_code = item["icd10Code"]
                            instance_death_by_disease_case_items.date_death_occurred = item["dateDeathOccurred"]
                            instance_death_by_disease_case_items.save()

                        # Death by Disease Case Out of Faciity lines

                    # Death outside at Facility
                    if message_type == "DDCOUT":
                        instance_death_by_disease_case_not_at_facility = core_models.DeathByDiseaseCaseNotAtFacility()
                        instance_death_by_disease_case_not_at_facility.transaction_id = transaction_id
                        instance_death_by_disease_case_not_at_facility.org_name = facility_name
                        instance_death_by_disease_case_not_at_facility.facility_hfr_code = facility_hfr_code
                        instance_death_by_disease_case_not_at_facility.save()

                        for item in items:
                            instance_death_by_disease_case_items_not_at_facility = core_models.DeathByDiseaseCaseNotAtFacilityItems()
                            instance_death_by_disease_case_items_not_at_facility.death_by_disease_case_not_at_facility_id = instance_death_by_disease_case_not_at_facility.id
                            instance_death_by_disease_case_items_not_at_facility.place_of_death_id = item["placeOfDeathID"]
                            instance_death_by_disease_case_items_not_at_facility.gender = item["gender"]
                            instance_death_by_disease_case_items_not_at_facility.date_of_birth = item["dob"]
                            instance_death_by_disease_case_items_not_at_facility.icd_10_code = item["icd10Code"]
                            instance_death_by_disease_case_items_not_at_facility.date_death_occurred = item["dateDeathOccurred"]
                            instance_death_by_disease_case_items_not_at_facility.death_id = item["deathId"]
                            instance_death_by_disease_case_items_not_at_facility.save()

                        # Bed Occupany parent lines

                    # Bed Occupancy
                    if message_type == "BEDOCC":
                        instance_bed_occupancy = core_models.BedOccupancy()
                        instance_bed_occupancy.transaction_id = transaction_id
                        instance_bed_occupancy.org_name = facility_name
                        instance_bed_occupancy.facility_hfr_code = facility_hfr_code
                        instance_bed_occupancy.save()

                        for item in items:
                            instance_bed_occupancy_items = core_models.BedOccupancyItems()

                            instance_bed_occupancy_items.bed_occupancy_id = instance_bed_occupancy.id
                            instance_bed_occupancy_items.ward_id = item["wardId"]
                            instance_bed_occupancy_items.ward_name = item["wardName"]
                            instance_bed_occupancy_items.patient_id = item["patId"]
                            instance_bed_occupancy_items.admission_date = item["admissionDate"]
                            instance_bed_occupancy_items.discharge_date = item["dischargeDate"]
                            instance_bed_occupancy.save()

                        # Revenue received parent lines

                    # Revenue
                    if message_type == "REV":
                        instance_revenue_received = core_models.RevenueReceived()
                        instance_revenue_received.transaction_id = transaction_id
                        instance_revenue_received.org_name = facility_name
                        instance_revenue_received.facility_hfr_code = facility_hfr_code
                        instance_revenue_received.save()

                        for item in items:
                            instance_revenue_received_items = core_models.RevenueReceivedItems()
                            instance_revenue_received_items.revenue_received_id = instance_revenue_received.id
                            instance_revenue_received_items.system_trans_id = item["systemTransId"]
                            instance_revenue_received_items.transaction_date = item["transactionDate"]
                            instance_revenue_received_items.patient_id = item["patId"]
                            instance_revenue_received_items.gender = item["gender"]
                            instance_revenue_received_items.date_of_birth = item["dob"]
                            instance_revenue_received_items.med_svc_code = item["medSvcCode"]
                            instance_revenue_received_items.payer_id = item["payerId"]
                            instance_revenue_received_items.exemption_category_id = item["exemptionCategoryId"]
                            instance_revenue_received_items.billed_amount = item["billedAmount"]
                            instance_revenue_received_items.waived_amount = item["waivedAmount"]
                            instance_revenue_received_items.service_provider_ranking_id = item["serviceProviderRankingId"]
                            instance_revenue_received_items.save()


def update_transaction_summary(transaction_id):
    transaction = validation_management_models.TransactionSummary.objects.get(id=transaction_id)
    transaction.total_passed += 1
    transaction.total_failed -= 1
    transaction.save()


@app.task
def calculate_and_save_bed_occupancy_rate():
    date_week_ago = datetime.today() - timedelta(days=60)
    bed_occupancy_items = core_models.BedOccupancyItems.objects.filter(admission_date__gte=date_week_ago.strftime("%Y-%m-%d"))

    admission_date = date_week_ago.strftime("%Y-%m-%d")
    discharge_date = datetime.now().strftime("%Y-%m-%d")

    if bed_occupancy_items is not None:
        for item in bed_occupancy_items:
            bed_occupancy_id = item.bed_occupancy_id
            bed_occupancy = core_models.BedOccupancy.objects.get(id=bed_occupancy_id)
            facility_hfr_code = bed_occupancy.facility_hfr_code

            instance_ward = master_data_models.Ward.objects.filter(local_ward_id=item.ward_id,
                                                                   facility__facility_hfr_code=facility_hfr_code).first()

            if instance_ward is not None:
                # Get Patient admission period to add days to it
                instance_patient = core_models.BedOccupancyReport.objects.filter(patient_id=item.patient_id,
                                                                                 admission_date=item.admission_date)
                if instance_patient.count() == 0:
                    get_patient_admission_discharge_period = core_models.BedOccupancyItems.objects.filter(
                        patient_id=item.patient_id, admission_date=item.admission_date,
                        discharge_date=item.discharge_date).first()

                    # Patient has does not have both admission and discharge dates
                    if get_patient_admission_discharge_period is None:
                        get_patient_admission_period = core_models.BedOccupancyItems.objects.filter(
                            patient_id=item.patient_id,
                            admission_date=item.admission_date).first()
                        # Patient has admission date only
                        if get_patient_admission_period is not None:
                            admission_date = get_patient_admission_period.admission_date
                            discharge_date = bed_occupancy_items.last().admission_date
                        else:
                            get_patient_discharge_period = core_models.BedOccupancyItems.objects.filter(
                                patient_id=item.patient_id,
                                discharge_date=item.discharge_date).first()
                            # Patient has discharge date only
                            if get_patient_discharge_period is not None:
                                admission_date = bed_occupancy_items.first().admission_date
                                discharge_date = get_patient_discharge_period.discharge_date
                    # Patient has both admission and discharge dates
                    else:
                        admission_date = get_patient_admission_discharge_period.admission_date
                        discharge_date = get_patient_admission_discharge_period.discharge_date
                else:
                    pass
                try:
                    bed_occupancy_rate = 1 / int(instance_ward.number_of_beds) * 100

                    create_bed_occupancy_report_record(discharge_date, admission_date, item, bed_occupancy_rate,
                                                       facility_hfr_code)

                except Exception as e:
                    print(e)


def create_bed_occupancy_report_record(discharge_date, admission_date, item, bed_occupancy_rate, facility_hfr_code):
    for x in range(int((discharge_date - admission_date).days)):
        instance_bed_occupancy_report = core_models.BedOccupancyReport()
        instance_bed_occupancy_report.patient_id = item.patient_id
        instance_bed_occupancy_report.date = item.admission_date + timedelta(days=x)
        instance_bed_occupancy_report.admission_date = item.admission_date
        instance_bed_occupancy_report.ward_id = item.ward_id
        instance_bed_occupancy_report.ward_name = item.ward_name
        instance_bed_occupancy_report.bed_occupancy = bed_occupancy_rate
        instance_bed_occupancy_report.facility_hfr_code = facility_hfr_code
        instance_bed_occupancy_report.save()
