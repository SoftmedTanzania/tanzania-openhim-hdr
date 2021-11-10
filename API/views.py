from rest_framework import viewsets, status
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from .serializers import TransactionSummarySerializer, IncomingDeathByDiseaseCaseAtTheFacilitySerializer, \
    DeathByDiseaseCaseAtFacilityItemsSerializer, \
    DeathByDiseaseCaseNotAtFacilityItemsSerializer, RevenueReceivedItemsSerializer,BedOccupancyItemsSerializer, \
    ServiceReceivedItemsSerializer, IncomingDeathByDiseaseCaseNotAtTheFacilitySerializer, \
    IncomingServicesReceivedSerializer, IncomingBedOccupancySerializer, IncomingRevenueReceivedSerializer, \
    ICD10CodeCategorySerializer, CPTCodeCategorySerializer, ClaimsSerializer, IncomingClaimsSerializer, UserLoginSerializer
from Core.models import RevenueReceived, DeathByDiseaseCaseAtFacility, \
    DeathByDiseaseCaseNotAtFacility,ServiceReceived, BedOccupancy, RevenueReceivedItems, ServiceReceivedItems, \
    DeathByDiseaseCaseAtFacilityItems, DeathByDiseaseCaseNotAtFacilityItems, BedOccupancyItems
from API import validators as validators
from ValidationManagement import models as validation_management_models
from TerminologyServicesManagement import models as terminology_services_management
from NHIF import models as nhif_models
import datetime as dt
from dateutil.relativedelta import relativedelta
import json


# Create your views here.
class TransactionSummaryView(viewsets.ModelViewSet):
    queryset = validation_management_models.TransactionSummary.objects.all()
    serializer_class = TransactionSummarySerializer
    permission_classes = (IsAuthenticated, )


class ServiceReceivedView(viewsets.ModelViewSet):
    queryset = ServiceReceived.objects.all()
    serializer_class = IncomingServicesReceivedSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            print("serializer is valid")
            result = validators.validate_received_payload(dict(serializer.data))
            transaction_status = result["transaction_status"]
            transaction_id = result["transaction_id"]

            if transaction_status is False:
                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.perform_create(request, serializer, transaction_id)

                headers = self.get_success_headers(serializer.data)
                response = {"message": "Success", "status": status.HTTP_200_OK}

                return Response(response, headers=headers)
        else:
            print(serializer.errors)
            print("serializer is not valid")
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer, transaction_id):

        # validate payload
        instance_service_received = ServiceReceived()

        instance_service_received.transaction_id = transaction_id
        instance_service_received.org_name = serializer.data["orgName"]
        instance_service_received.facility_hfr_code = serializer.data["facilityHfrCode"]
        instance_service_received.save()

        status = []

        for val in serializer.data["items"]:
            try:
                instance_service_received_item = ServiceReceivedItems()

                instance_service_received_item.service_received_id= instance_service_received.id
                instance_service_received_item.department_name = val["deptName"]
                instance_service_received_item.department_id = val["deptId"]

                if val["patId"] is None:
                    instance_service_received_item.patient_id = 0
                else:
                    instance_service_received_item.patient_id = val["patId"]

                instance_service_received_item.gender = val["gender"]
                instance_service_received_item.date_of_birth = validators.convert_date_formats(val["dob"])
                instance_service_received_item.med_svc_code = val["medSvcCode"]
                instance_service_received_item.confirmed_diagnosis = val["confirmedDiagnosis"]
                instance_service_received_item.differential_diagnosis = val["differentialDiagnosis"]
                instance_service_received_item.provisional_diagnosis = val["provisionalDiagnosis"]
                instance_service_received_item.service_date = validators.convert_date_formats(val["serviceDate"])
                instance_service_received_item.service_provider_ranking_id = val["serviceProviderRankingId"]
                instance_service_received_item.visit_type = val["visitType"]

                instance_service_received_item.save()

                status_code = 200
                status.append(status_code)

            except:
                pass

        return  status

    def list(self, request):
        queryset = ServiceReceivedItems.objects.all().order_by('-id')
        serializer = ServiceReceivedItemsSerializer(queryset, many=True)
        return Response(serializer.data)


class DeathByDiseaseCaseAtFacilityView(viewsets.ModelViewSet):
    queryset = DeathByDiseaseCaseAtFacility.objects.all()
    serializer_class = IncomingDeathByDiseaseCaseAtTheFacilitySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            result = validators.validate_received_payload(dict(serializer.data))
            transaction_status = result["transaction_status"]
            transaction_id = result["transaction_id"]


            if transaction_status is False:
                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.perform_create(request, serializer, transaction_id)

                headers = self.get_success_headers(serializer.data)
                response = {"message": "Success", "status": status.HTTP_200_OK}

                return Response(response, headers=headers)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer, transaction_id):

        # validate payload
        instance_death_by_disease_case_at_facility = DeathByDiseaseCaseAtFacility()

        instance_death_by_disease_case_at_facility.transaction_id = transaction_id
        instance_death_by_disease_case_at_facility.org_name = serializer.data["orgName"]
        instance_death_by_disease_case_at_facility.facility_hfr_code = serializer.data["facilityHfrCode"]
        instance_death_by_disease_case_at_facility.save()

        status = []

        for val in serializer.data["items"]:
            # validate payload
            try:
                instance_death_by_disease_case_at_facility_item = DeathByDiseaseCaseAtFacilityItems()

                instance_death_by_disease_case_at_facility_item.death_by_disease_case_at_facility_id = instance_death_by_disease_case_at_facility.id
                instance_death_by_disease_case_at_facility_item.ward_name = val["wardName"]
                instance_death_by_disease_case_at_facility_item.ward_id = val["wardId"]
                instance_death_by_disease_case_at_facility_item.patient_id = val["patId"]
                instance_death_by_disease_case_at_facility_item.first_name = val["firstName"]
                instance_death_by_disease_case_at_facility_item.middle_name = val["middleName"]
                instance_death_by_disease_case_at_facility_item.last_name = val["lastName"]
                instance_death_by_disease_case_at_facility_item.gender = val["gender"]
                instance_death_by_disease_case_at_facility_item.date_of_birth = validators.convert_date_formats(val["dob"])
                instance_death_by_disease_case_at_facility_item.cause_of_death = val["causeOfDeath"]
                instance_death_by_disease_case_at_facility_item.immediate_cause_of_death = val["immediateCauseOfDeath"]
                instance_death_by_disease_case_at_facility_item.underlying_cause_of_death = val["underlyingCauseOfDeath"]
                instance_death_by_disease_case_at_facility_item.date_death_occurred = validators.convert_date_formats(val["dateDeathOccurred"])

                instance_death_by_disease_case_at_facility_item.save()

                status_code = 200
                status.append(status_code)
            except:
                pass

        return status

    def list(self, request):
        queryset = DeathByDiseaseCaseAtFacilityItems.objects.all().order_by('-id')
        serializer = DeathByDiseaseCaseAtFacilityItemsSerializer(queryset, many=True)
        return Response(serializer.data)


class DeathByDiseaseCaseNotAtFacilityView(viewsets.ModelViewSet):
    queryset = DeathByDiseaseCaseNotAtFacility.objects.all()
    serializer_class = IncomingDeathByDiseaseCaseNotAtTheFacilitySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            result = validators.validate_received_payload(dict(serializer.data))
            transaction_status = result["transaction_status"]
            transaction_id = result["transaction_id"]

            if transaction_status is False:

                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.perform_create(request, serializer, transaction_id)

                headers = self.get_success_headers(serializer.data)
                response = {"message": "Success", "status": status.HTTP_200_OK}

                return Response(response, headers=headers)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer, transaction_id):
        # validate payload
        instance_death_by_disease_case_not_at_facility = DeathByDiseaseCaseNotAtFacility()

        instance_death_by_disease_case_not_at_facility.transaction_id = transaction_id
        instance_death_by_disease_case_not_at_facility.org_name = serializer.data["orgName"]
        instance_death_by_disease_case_not_at_facility.facility_hfr_code = serializer.data["facilityHfrCode"]
        instance_death_by_disease_case_not_at_facility.save()

        status = []
        for val in serializer.data["items"]:
            # validate payload
            try:
                instance_death_by_disease_case_not_at_facility_items = DeathByDiseaseCaseNotAtFacilityItems()

                instance_death_by_disease_case_not_at_facility_items.place_of_death_id = val["placeOfDeathId"]
                instance_death_by_disease_case_not_at_facility_items.death_by_disease_case_not_at_facility_id=instance_death_by_disease_case_not_at_facility.id
                instance_death_by_disease_case_not_at_facility_items.gender = val["gender"]
                instance_death_by_disease_case_not_at_facility_items.date_of_birth = validators.convert_date_formats(val["dob"])
                instance_death_by_disease_case_not_at_facility_items.cause_of_death = val["causeOfDeath"]
                instance_death_by_disease_case_not_at_facility_items.immediate_cause_of_death = val["immediateCauseOfDeath"]
                instance_death_by_disease_case_not_at_facility_items.underlying_cause_of_death = val["underlyingCauseOfDeath"]
                instance_death_by_disease_case_not_at_facility_items.date_death_occurred = validators.convert_date_formats(val["dateDeathOccurred"])
                instance_death_by_disease_case_not_at_facility_items.death_id = val["deathId"]

                instance_death_by_disease_case_not_at_facility_items.save()
                status_code = 200
                status.append(status_code)
            except:
                pass

        return status

    def list(self, request):
        queryset = DeathByDiseaseCaseNotAtFacilityItems.objects.all().order_by('-id')
        serializer = DeathByDiseaseCaseNotAtFacilityItemsSerializer(queryset, many=True)
        return Response(serializer.data)


class RevenueReceivedView(viewsets.ModelViewSet):
    queryset = RevenueReceived.objects.all()
    serializer_class = IncomingRevenueReceivedSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            result = validators.validate_received_payload(dict(serializer.data))
            transaction_status = result["transaction_status"]
            transaction_id = result["transaction_id"]

            if transaction_status is False:

                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.perform_create(request, serializer, transaction_id)

                headers = self.get_success_headers(serializer.data)
                response = {"message": "Success", "status": status.HTTP_200_OK}

                return Response(response, headers=headers)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer, transaction_id):
        # validate payload
        instance_revenue_received = RevenueReceived()

        instance_revenue_received.transaction_id = transaction_id
        instance_revenue_received.org_name = serializer.data["orgName"]
        instance_revenue_received.facility_hfr_code = serializer.data["facilityHfrCode"]
        instance_revenue_received.save()

        status = []
        for val in serializer.data["items"]:
            # validate payload
            try:
                instance_revenue_received_items = RevenueReceivedItems()

                instance_revenue_received_items.system_trans_id = val["systemTransId"]
                instance_revenue_received_items.transaction_date = validators.convert_date_formats(val["transactionDate"])

                if val["patId"] is None:
                    instance_revenue_received_items.patient_id = 0
                else:
                    instance_revenue_received_items.patient_id = val["patId"]

                instance_revenue_received_items.gender = val["gender"]
                instance_revenue_received_items.revenue_received_id = instance_revenue_received.id
                instance_revenue_received_items.date_of_birth = validators.convert_date_formats(val["dob"])
                instance_revenue_received_items.med_svc_code = val["medSvcCode"]
                instance_revenue_received_items.payer_id = val["payerId"]
                instance_revenue_received_items.exemption_category_id = val["exemptionCategoryId"]
                instance_revenue_received_items.billed_amount = val["billedAmount"]
                instance_revenue_received_items.waived_amount = val["waivedAmount"]
                instance_revenue_received_items.service_provider_ranking_id = val["serviceProviderRankingId"]

                instance_revenue_received_items.save()
                status_code = 200
                status.append(status_code)
            except:
                pass

        return status

    def list(self, request):
        queryset = RevenueReceivedItems.objects.all().order_by('-id')
        serializer = RevenueReceivedItemsSerializer(queryset, many=True)
        return Response(serializer.data)


class BedOccupancyView(viewsets.ModelViewSet):
    queryset = BedOccupancy.objects.all()
    serializer_class = IncomingBedOccupancySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            result = validators.validate_received_payload(dict(serializer.data))
            transaction_status = result["transaction_status"]
            transaction_id = result["transaction_id"]

            if transaction_status is False:
                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.perform_create(request, serializer, transaction_id)

                headers = self.get_success_headers(serializer.data)
                response = {"message": "Success", "status": status.HTTP_200_OK}

                return Response(response, headers=headers)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer, transaction_id):
        # validate payload
        instance_bed_occupancy = BedOccupancy()

        instance_bed_occupancy.transaction_id = transaction_id
        instance_bed_occupancy.org_name = serializer.data["orgName"]
        instance_bed_occupancy.facility_hfr_code = serializer.data["facilityHfrCode"]
        instance_bed_occupancy.save()

        status = []

        for val in serializer.data["items"]:
            try:
                print(validators.convert_date_formats(val["dischargeDate"]))
                instance_bed_occupancy_item = BedOccupancyItems()
                instance_bed_occupancy_item.patient_id = val["patId"]
                instance_bed_occupancy_item.bed_occupancy_id = instance_bed_occupancy.id
                instance_bed_occupancy_item.admission_date = validators.convert_date_formats(val["admissionDate"])
                instance_bed_occupancy_item.discharge_date = validators.convert_date_formats(val["dischargeDate"])
                instance_bed_occupancy_item.ward_name = val["wardName"]
                instance_bed_occupancy_item.ward_id = val["wardId"]

                instance_bed_occupancy_item.save()

                status_code = 200
                status.append(status_code)

            except:
                pass

        return status

    def list(self, request):
        queryset = BedOccupancyItems.objects.all().order_by('-id')
        serializer = BedOccupancyItemsSerializer(queryset, many=True)
        return Response(serializer.data)


class ICD10View(viewsets.ModelViewSet):
    queryset = terminology_services_management.ICD10CodeCategory.objects.all()
    serializer_class = ICD10CodeCategorySerializer
    permission_classes = ()

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            process_status = self.perform_create(request, serializer)

            if process_status is True:
                response = {"message": "Success", "status": status.HTTP_200_OK}
            else:
                response = {"message": "Fail", "status": status.HTTP_400_BAD_REQUEST}

            headers = self.get_success_headers(serializer.data)
            return Response(response, headers=headers)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer):
        # validate payload
        data = serializer.data

        for x in data:
            identifier = x["identifier"]
            description = x["description"]

            sub_categories = x["sub_category"]

            category = terminology_services_management.ICD10CodeCategory.objects.filter(
                identifier=identifier).first()

            if category is None:
                # # insert category
                instance_category = terminology_services_management.ICD10CodeCategory()
                instance_category.identifier = identifier
                instance_category.description = description
                instance_category.save()
            else:
                pass

            for sub_category in sub_categories:
                identifier = sub_category["identifier"]
                description = sub_category["description"]

                codes = sub_category["code"]

                sub_category = terminology_services_management.ICD10CodeSubCategory.objects.filter(
                    identifier=identifier).first()

                if sub_category is None:
                    # # insert sub category
                    instance_sub_category = terminology_services_management.ICD10CodeSubCategory()

                    last_category = terminology_services_management.ICD10CodeCategory.objects.all().last()
                    instance_sub_category.identifier = identifier
                    instance_sub_category.description = description
                    instance_sub_category.category_id = last_category.id
                    instance_sub_category.save()
                else:
                    pass

                # loop through the sub sub categories
                for code in codes:
                    description = code["description"]
                    identifier = code["code"]

                    sub_codes = code["sub_code"]

                    code = terminology_services_management.ICD10Code.objects.filter(code=identifier).first()

                    if code is None:
                        # # insert icd code
                        instance_icd_code = terminology_services_management.ICD10Code()

                        last_sub_category = terminology_services_management.ICD10CodeSubCategory.objects.all().last()
                        instance_icd_code.sub_category_id = last_sub_category.id
                        instance_icd_code.code = identifier
                        instance_icd_code.description = description
                        instance_icd_code.save()
                    else:
                        pass

                    for sub_code in sub_codes:
                        identifier = sub_code["sub_code"]
                        description = sub_code["description"]

                        sub_code = terminology_services_management.ICD10SubCode.objects.filter(
                            sub_code=identifier).first()

                        if sub_code is None:
                            # insert icd sub code
                            instance_icd_sub_code = terminology_services_management.ICD10SubCode()

                            last_code = terminology_services_management.ICD10Code.objects.all().last()
                            instance_icd_sub_code.code_id = last_code.id
                            instance_icd_sub_code.sub_code = identifier
                            instance_icd_sub_code.description = description
                            instance_icd_sub_code.save()
                        else:
                            pass

        return True

    def list(self, request):
        queryset = terminology_services_management.ICD10CodeCategory.objects.all().order_by('-id')
        serializer = ICD10CodeCategorySerializer(queryset, many=True)
        return Response(serializer.data)


class CPTCodeView(viewsets.ModelViewSet):
    queryset = terminology_services_management.CPTCodeCategory.objects.all()
    serializer_class = CPTCodeCategorySerializer
    permission_classes = ()


class ClaimsView(viewsets.ModelViewSet):
    queryset = nhif_models.Claims.objects.all()
    serializer_class = IncomingClaimsSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(request, serializer)

            headers = self.get_success_headers(serializer.data)
            response = {"message": "Success", "status": status.HTTP_200_OK}

            return Response(response, headers=headers)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer):
        # validate payload
        for val in serializer.data:
            instance_claim = nhif_models.Claims()

            instance_claim.facility_hfr_code = val["facilityHfrCode"]
            instance_claim.claimed_amount = val["claimedAmount"]
            instance_claim.period = val["period"]
            instance_claim.date = get_last_day_of_month(val["period"])
            instance_claim.computed_amount = val["computedAmount"]
            instance_claim.accepted_amount = val["acceptedAmount"]
            instance_claim.loan_deductions = val["loanDeductions"]
            instance_claim.other_deductions = val["otherDeductions"]
            instance_claim.paid_amount = val["paidAmount"]
            instance_claim.save()

        return status

    def list(self, request):
        queryset = nhif_models.Claims.objects.all().order_by('-id')
        serializer = ClaimsSerializer(queryset, many=True)
        return Response(serializer.data)


def get_last_day_of_month(claim_period):
    period = claim_period.split(sep="-", maxsplit=1)
    year = int(period[0])
    month = int(period[1])

    date_estimate = dt.datetime(year, month, 15)

    last_day_of_the_month = dt.datetime(date_estimate.year, (date_estimate + relativedelta(months=1)).month,
                                        1) - dt.timedelta(days=1)
    print(last_day_of_the_month.date())

    return last_day_of_the_month.date()



