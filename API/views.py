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
from UserManagement.views import main as user_management_views
from rest_framework.views import APIView


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
            if validators.validate_received_payload(dict(serializer.data)) is False:
                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.perform_create(request, serializer)

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

    def perform_create(self, request, serializer):

        # validate payload
        print("here now")
        instance_service_received = ServiceReceived()

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
                instance_service_received_item.icd_10_code = val["icd10Code"]
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
            if validators.validate_received_payload(dict(serializer.data)) is False:
                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
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
        instance_death_by_disease_case_at_facility = DeathByDiseaseCaseAtFacility()

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
                instance_death_by_disease_case_at_facility_item.icd_10_code = val["icd10Code"]
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
            if validators.validate_received_payload(dict(serializer.data)) is False:

                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
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
        instance_death_by_disease_case_not_at_facility = DeathByDiseaseCaseNotAtFacility()

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
                instance_death_by_disease_case_not_at_facility_items.icd_10_code = val["icd10Code"]
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
            if validators.validate_received_payload(dict(serializer.data)) is False:

                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
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
        instance_revenue_received = RevenueReceived()

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
            if validators.validate_received_payload(dict(serializer.data)) is False:
                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
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
        instance_bed_occupancy = BedOccupancy()

        instance_bed_occupancy.org_name = serializer.data["orgName"]
        instance_bed_occupancy.facility_hfr_code = serializer.data["facilityHfrCode"]
        instance_bed_occupancy.save()

        status = []
        for val in serializer.data["items"]:
            try:

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
