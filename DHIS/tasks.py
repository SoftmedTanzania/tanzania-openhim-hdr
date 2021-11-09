from celery import Celery
import requests
from decouple import config
from NHIF import models as nhif_models
from MasterData import models as master_data_models
from _datetime import datetime
from dateutil.relativedelta import relativedelta
from DHIS import models as dhis_models
import json

app = Celery()


def send_to_dhis(payload):
    dhis_url = config('DHIS_URL')
    response = requests.post(dhis_url, auth=(config('DHIS_USERNAME'), config('DHIS_PASSWORD')),
                             json=payload)
    return response


@app.task()
def create_claims_payload():
    current_date = datetime.now().date()
    month_ago = current_date - relativedelta(months=1)

    facilities = master_data_models.Facility.objects.all()

    data_values = []

    for facility in facilities:
        facility_hfr_code =  facility.facility_hfr_code
        
        claims = nhif_models.Claims.objects.filter(facility_hfr_code=facility_hfr_code, date__gte=month_ago,
                                                   date__lte=current_date)

        if claims.count() > 0:
            for claim in claims:
                # get data elements
                data_elements = dhis_models.DataElement.objects.all()

                period = claim.period

                for data_element in data_elements:
                    data_element_uid = data_element.data_element_uid
                    data_element_sys_name = data_element.data_element_sys_name

                    value = 0

                    if data_element_sys_name == "claimed_amount":
                        value = str(claim.claimed_amount)
                    elif data_element_sys_name == "computed_amount":
                        value = str(claim.computed_amount)
                    elif data_element_sys_name == "accepted_amount":
                        value = str(claim.accepted_amount)
                    elif data_element_sys_name == "loan_deductions":
                        value = str(claim.loan_deductions)
                    elif data_element_sys_name == "other_deductions":
                        value = str(claim.other_deductions)
                    elif data_element_sys_name == "paid_amount":
                        value = str(claim.paid_amount)
                    else:
                        pass

                    data_value = {
                        "dataElement": data_element_uid,
                        "period":str(period),
                        "orgUnit": facility_hfr_code,
                        "value": float(value)
                    }

                    data_values.append(data_value)

            if data_values is not None:
                send_to_dhis(json.dumps(data_values))

        else:
            pass

