# from django.urls import path, reverse
# from rest_framework.test import APITestCase, URLPatternsTestCase
# from .views import ClientEventView
# from rest_framework import status
#
#
# # Create your tests here.
# class ClientEventTestCase(APITestCase, URLPatternsTestCase):
#     urlpatterns = [
#         path('clients_events/', ClientEventView.as_view(), name='clients_events'),
#     ]
#
#     def test_post_client_event(self):
#         """Ensure we can send an object to the endpoint."""
#         url = reverse('clients_events')
#         data = {
#             "hdrClient": {
#                 "openHimClientId": "csv-sync-service",
#                 "name": "csv-sync-service"
#             },
#             "hdrEvents": [
#                 {
#                     "eventType": "save-service-received",
#                     "eventDate": "Dec 29, 2020, 4:33:45 PM",
#                     "openHimClientId": "csv-sync-service",
#                     "mediatorVersion": "0.1.0",
#                     "payload": {
#                         "messageType": "SVCREC",
#                         "orgName": "Masana",
#                         "localOrgID": "108627-1",
#                         "deptName": "Radiology",
#                         "deptID": "80",
#                         "patID": "1",
#                         "gender": "Male",
#                         "dob": "19900131",
#                         "medSvcCode": "002923, 00277, 002772",
#                         "icd10Code": "A17.8, M60.1",
#                         "serviceDate": "20201224"
#                     }
#                 }
#             ]
#         }
#
#         response = self.client.post(url,data ,format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)