from celery import Celery
import requests
from decouple import config

app = Celery()

def send_to_dhis(payload):
    dhis_url = config('DHIS_URL')
    response = requests.post(dhis_url, auth=(config('DHIS_USERNAME'), config('DHIS_PASSWORD')), json=payload)
    response_data = response.json()
    return response_data


