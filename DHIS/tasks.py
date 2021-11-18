from celery import Celery
import requests
from decouple import config
from NHIF import models as nhif_models
from MasterData import models as master_data_models
from _datetime import datetime
from dateutil.relativedelta import relativedelta
from DHIS import models as dhis_models
import json
from django.db.models import Sum
import calendar
from Core import models as core_models

app = Celery()


def send_to_dhis(payload):
    dhis_url = config('HIM_DHIS_URL')
    response = requests.post(dhis_url, auth=(config('HIM_USERNAME'), config('HIM_PASSWORD')),
                             json=payload)
    return response


@app.task()
def create_claims_payload(request):
    current_date = datetime.now().date()
    month_ago = current_date - relativedelta(months=1)

    # date_from = month_ago.replace(day=1)
    date_from = "2020-01-01"
    date_to = "2021-12-30"
    # date_to = get_end_date_by_month(date_from)

    facilities = master_data_models.Facility.objects.all().values('facility_hfr_code').distinct()

    data_values = []

    for facility in facilities:
        facility_hfr_code =  facility['facility_hfr_code']

        overall_claims = nhif_models.Claims.objects.filter(facility_hfr_code=facility_hfr_code,
                                                           date__gte=date_from,
                                                           date__lte=date_to)

        if overall_claims.count() > 0:
            claimed_amount = nhif_models.Claims.objects.filter(facility_hfr_code=facility_hfr_code,
                                                               date__gte=date_from,
                                                               date__lte=date_to).values('facility_hfr_code', 'period'). \
                annotate(total_claimed_amount=Sum('claimed_amount'))


            computed_amount = nhif_models.Claims.objects.filter(facility_hfr_code=facility_hfr_code,
                                                                date__gte=date_from,
                                                                date__lte=date_to).values('facility_hfr_code','period'). \
                annotate(total_computed_amount=Sum('computed_amount'))

            accepted_amount = nhif_models.Claims.objects.filter(facility_hfr_code=facility_hfr_code,
                                                                date__gte=date_from,
                                                                date__lte=date_to).values('facility_hfr_code','period'). \
                annotate(total_accepted_amount=Sum('accepted_amount'))

            loan_deductions = nhif_models.Claims.objects.filter(facility_hfr_code=facility_hfr_code,
                                                                date__gte=date_from,
                                                                date__lte=date_to).values('facility_hfr_code','period'). \
                annotate(total_loan_deductions=Sum('loan_deductions'))

            other_deductions = nhif_models.Claims.objects.filter(facility_hfr_code=facility_hfr_code,
                                                                 date__gte=date_from,
                                                                 date__lte=date_to).values('facility_hfr_code','period'). \
                annotate(total_other_deductions=Sum('other_deductions'))

            paid_amount = nhif_models.Claims.objects.filter(facility_hfr_code=facility_hfr_code,
                                                            date__gte=date_from,
                                                            date__lte=date_to).values('facility_hfr_code','period'). \
                annotate(total_paid_amount=Sum('paid_amount'))


            data_elements = dhis_models.DataElement.objects.all()

            for data_element in data_elements:
                data_element_uid = data_element.data_element_uid
                data_element_sys_name = data_element.data_element_sys_name

                value =  0
                period = ''

                if data_element_sys_name == "claimed_amount":
                    if claimed_amount.count() > 0:
                        value = claimed_amount.first()["total_claimed_amount"]
                        period = claimed_amount.first()["period"]
                elif data_element_sys_name == "computed_amount":
                    if computed_amount.count() > 0:
                        value = computed_amount.first()["total_computed_amount"]
                        period = computed_amount.first()["period"]
                elif data_element_sys_name == "accepted_amount":
                    if accepted_amount.count() > 0:
                        value = accepted_amount.first()["total_accepted_amount"]
                        period = accepted_amount.first()["period"]
                elif data_element_sys_name == "loan_deductions":
                    if loan_deductions.count() > 0:
                        value = loan_deductions.first()["total_loan_deductions"]
                        period = loan_deductions.first()["period"]
                elif data_element_sys_name == "other_deductions":
                    if other_deductions.count() > 0:
                        value = other_deductions.first()["total_other_deductions"]
                        period = other_deductions.first()["period"]
                elif data_element_sys_name == "paid_amount":
                    if paid_amount.count() > 0:
                        value = paid_amount.first()["total_paid_amount"]
                        period = paid_amount.first()["period"]
                else:
                    pass

                data_dict = dict()
                data_dict["dataElement"] = data_element_uid
                data_dict["period"] = str(period).replace('-', '')
                data_dict["orgUnit"] = facility_hfr_code
                data_dict["value"] = float(value)

                data_values.append(data_dict)

            if len(data_values) > 0:
                payload = {
                    "dataValues":data_values
                }
                response = send_to_dhis(payload)
                # print(response.status_code)
                # print(response.content)
                data_values = []


@app.task()
def create_ddc_payload(request):
    current_date = datetime.now().date()
    month_ago = current_date - relativedelta(months=1)

    date_from = month_ago.replace(day=1)
    date_to = get_end_date_by_month(date_from)

    facilities = master_data_models.Facility.objects.all().values('facility_hfr_code').distinct()

    data_values = []

    for facility in facilities:
        facility_hfr_code = facility['facility_hfr_code']

        deaths_occured = core_models.DeathByDiseaseCaseAtFacilityItems.objects.filter(death_by_disease_case_at_facility__facility_hfr_code=facility_hfr_code,
                                                                                      date_death_occurred__gte=date_from,
                                                                                      date_death_occurred__lte=date_to)

        client_data_values = []
        if deaths_occured.count() > 0:
            for death in  deaths_occured:
                client_name = death.first_name + " " + death.middle_name + ' ' + death.last_name
                gender = death.gender
                date_of_birth = death.date_of_birth

                date_death_occurred = death.date_death_occurred

                cause_of_death = death.cause_of_death
                immediate_cause_of_death = death.immediate_cause_of_death
                underlying_cause_of_death = death.underlying_cause_of_death

                data_elements = dhis_models.DataElement.objects.all()

                for data_element in data_elements:
                    data_element_uid = data_element.data_element_uid
                    data_element_sys_name = data_element.data_element_sys_name

                    value = 0

                    if data_element_sys_name == "date_death_occurred":
                        value = date_death_occurred
                    elif data_element_sys_name == "client_name":
                        value = client_name
                    elif data_element_sys_name == "gender":
                        value = gender
                    elif data_element_sys_name == "date_of_birth":
                        value = date_of_birth
                    elif data_element_sys_name == "place_of_death":
                        value = 'Health Facility'
                    elif data_element_sys_name == "immediate_cause_of_death":
                        value = immediate_cause_of_death
                    elif data_element_sys_name == "underlying_cause_of_death":
                        value = underlying_cause_of_death
                    else:
                        pass

                    data_values_dict = dict()
                    data_values_dict["dataElement"] = data_element_uid
                    data_values_dict["value"] = float(value)

                    client_data_values.append(data_values_dict)

    if len(data_values) > 0:
        payload = {
            "dataValues": data_values
        }
        response = send_to_dhis(payload)
        print(response.status_code)
        print(response.content)
        data_values = []


def get_end_date_by_month(start_date):
    month = start_date.month
    year = start_date.year

    end_date_tuple = calendar.monthrange(year, month)

    end_day = end_date_tuple[1]

    end_date = str(year) + "-" + str(month) + "-" + str(end_day)

    return datetime.strptime(end_date, '%Y-%m-%d').date()