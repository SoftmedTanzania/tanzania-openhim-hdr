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


@app.task
def save_payload_from_csv():
    root_path = "uploads"
    i = 0
    for subdir, _, _ in os.walk(root_path):
        for file in os.listdir(subdir):
            print("for function here")
            file_path = "" + root_path + "/" + file
            with open(file_path, 'r') as fp:
                print("open file here")
                lines = csv.reader(fp, delimiter=',')

                imported_payload = core_views.regenerate_services_received_json_payload(lines)

                if validators.validate_received_payload(json.loads(imported_payload)) is False:
                    print("validation failed")
                else:
                    print("validation successful")
                    for line in lines:
                        if i == 1:
                            message_type = str(line[0]).upper()
                            facility_hfr_code = line[1]
                            facility_name = line[2]

                            # Service received parents lines
                            if message_type == "SVCREC":
                                instance_service_received = core_models.ServiceReceived()
                                instance_service_received.org_name = facility_name
                                instance_service_received.facility_hfr_code = facility_hfr_code
                                instance_service_received.save()

                                # Death by Facility in facility parent lines
                            if message_type == "DDC":
                                instance_death_by_disease_case_at_facility = core_models.DeathByDiseaseCaseAtFacility()
                                instance_death_by_disease_case_at_facility.org_name = facility_name
                                instance_death_by_disease_case_at_facility.facility_hfr_code = facility_hfr_code
                                instance_death_by_disease_case_at_facility.save()

                                # Death by Disease Case Out of Faciity lines
                            if message_type == "DDCOUT":
                                instance_death_by_disease_case_not_at_facility = core_models.DeathByDiseaseCaseNotAtFacility()
                                instance_death_by_disease_case_not_at_facility.org_name = facility_name
                                instance_death_by_disease_case_not_at_facility.facility_hfr_code = facility_hfr_code
                                instance_death_by_disease_case_not_at_facility.save()
                                # Bed Occupany parent lines
                            if message_type == "BEDOCC":
                                instance_bed_occupancy = core_models.BedOccupancy()
                                instance_bed_occupancy.org_name = facility_name
                                instance_bed_occupancy.facility_hfr_code = facility_hfr_code
                                instance_bed_occupancy.save()

                                # Revenue received parent lines
                            if message_type == "REV":
                                instance_revenue_received = core_models.RevenueReceived()
                                instance_revenue_received.org_name = facility_name
                                instance_revenue_received.facility_hfr_code = facility_hfr_code
                                instance_revenue_received.save()

                        i += 1

                    for line in lines:
                        row = 0

                        if row == 0:
                            headers = line
                            row = row + 1
                        else:
                            new_line_details = {}
                            for i in range(len(headers)):
                                new_line_details[headers[i]] = line[i]

                            # save the transaction lines and message
                            if message_type == "SVCREC":

                                last_service_received = core_models.ServiceReceived.objects.all().last()
                                instance_service_received_items = core_models.ServiceReceivedItems()
                                instance_service_received_items.service_received_id = last_service_received.id
                                instance_service_received_items.department_name = line[3]
                                instance_service_received_items.department_id = line[4]
                                instance_service_received_items.patient_id = line[5]
                                instance_service_received_items.gender = line[6]
                                instance_service_received_items.date_of_birth = validators.convert_date_formats(line[7])
                                instance_service_received_items.med_svc_code = line[8]
                                instance_service_received_items.icd_10_code = line[9]
                                instance_service_received_items.service_date = validators.convert_date_formats(line[10])
                                instance_service_received_items.service_provider_ranking_id = line[11]
                                instance_service_received_items.visit_type = line[12]
                                instance_service_received_items.save()

                                # Update transactions
                                # update_transaction_summary(transaction_id)

                            elif message_type == "DDC":
                                last_death_at_facility = core_models.DeathByDiseaseCaseAtFacility.objects.all().last()
                                instance_death_by_disease_case_items = core_models.DeathByDiseaseCaseAtFacility()
                                instance_death_by_disease_case_items.death_by_disease_case_at_facility_id = last_death_at_facility.id
                                instance_death_by_disease_case_items.ward_id = line[3]
                                instance_death_by_disease_case_items.ward_name = line[4]
                                instance_death_by_disease_case_items.patient_id = line[5]
                                instance_death_by_disease_case_items.first_name = line[6]
                                instance_death_by_disease_case_items.middle_name = line[7]
                                instance_death_by_disease_case_items.last_name = line[8]
                                instance_death_by_disease_case_items.icd_10_code = line[9]
                                instance_death_by_disease_case_items.gender = line[10]
                                instance_death_by_disease_case_items.date_of_birth = line[11]
                                instance_death_by_disease_case_items.date_death_occurred = line[12]
                                instance_death_by_disease_case_items.save()

                            elif message_type == "DDCOUT":
                                last_death_outside_facility = core_models.DeathByDiseaseCaseNotAtFacility.objects.all().last()
                                instance_death_by_disease_case_items_not_at_facility = core_models.DeathByDiseaseCaseNotAtFacilityItems()

                                instance_death_by_disease_case_items_not_at_facility.death_by_disease_case_not_at_facility_id = last_death_outside_facility.id
                                instance_death_by_disease_case_items_not_at_facility.place_of_death_id = line[3]
                                instance_death_by_disease_case_items_not_at_facility.gender = line[4]
                                instance_death_by_disease_case_items_not_at_facility.date_of_birth = line[5]
                                instance_death_by_disease_case_items_not_at_facility.icd_10_code = line[6]
                                instance_death_by_disease_case_items_not_at_facility.date_death_occurred = line[7]
                                instance_death_by_disease_case_items_not_at_facility.death_id = line[8]
                                instance_death_by_disease_case_items_not_at_facility.save()


                            elif message_type == "BEDOCC":
                                last_bed_occupancy = core_models.BedOccupancy.objects.all().last()
                                instance_bed_occupancy_items = core_models.BedOccupancyItems()

                                instance_bed_occupancy_items.bed_occupancy_id = last_bed_occupancy.id
                                instance_bed_occupancy_items.ward_id = line[3]
                                instance_bed_occupancy_items.ward_name = line[4]
                                instance_bed_occupancy_items.patient_id = line(5)
                                instance_bed_occupancy_items.admission_date = line[6]
                                instance_bed_occupancy_items.discharge_date = line[7]

                                instance_bed_occupancy_items.save()

                            elif message_type == "REV":
                                last_revenue_received = core_models.RevenueReceived.objects.filter().last()
                                instance_revenue_received_items = core_models.RevenueReceivedItems()

                                instance_revenue_received_items.revenue_received_id = last_revenue_received.id
                                instance_revenue_received_items.system_trans_id = line(3)
                                instance_revenue_received_items.transaction_date = line(4)
                                instance_revenue_received_items.patient_id = line[5]
                                instance_revenue_received_items.gender = line[6]
                                instance_revenue_received_items.date_of_birth = line[7]
                                instance_revenue_received_items.med_svc_code = line[8]
                                instance_revenue_received_items.payer_id = line[9]
                                instance_revenue_received_items.exemption_category_id = line[10]
                                instance_revenue_received_items.billed_amount = line[11]
                                instance_revenue_received_items.waived_amount = line[12]
                                instance_revenue_received_items.service_provider_ranking_id = line[13]
                                instance_revenue_received_items.save()

                            else:
                                return False

                        row = row + 1

                    fp.close()
                    os.remove(file_path)
                    i = 0




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
