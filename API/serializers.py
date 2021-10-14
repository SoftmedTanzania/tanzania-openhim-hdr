from django.contrib.auth.models import User
from UserManagement import models as user_management_models
from ValidationManagement import models as validation_management_models
from Core import models as core_models
from TerminologyServicesManagement import models as terminology_services_management
from rest_framework import serializers
from NHIF import models as nhif_models


class ProfileSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = user_management_models.Profile
        fields = ('user','birth_date', 'location','reg_id')


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'profile')


class TokenSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(many=False, read_only=True)  # this is add by myself.

    class Meta:
        model = user_management_models.TokenModel
        fields = ('key', 'user')  # there I add the `user` field ( this is my need data ).


class TransactionSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = validation_management_models.TransactionSummary
        fields = '__all__'


class ServiceReceivedItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.ServiceReceivedItems
        fields = ('service_received', 'department_name','department_id', 'patient_id', 'gender', 'date_of_birth',
                  'med_svc_code', 'icd_10_code', 'service_date','service_provider_ranking_id','visit_type' )


class ServiceReceivedSerializer(serializers.ModelSerializer):
    items = ServiceReceivedItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.ServiceReceived
        fields = ('org_name','facility_hfr_code','items')


class IncomingServiceReceivedItemsSerializer(serializers.Serializer):
    deptName = serializers.CharField(max_length=255)
    deptId = serializers.CharField(max_length=255)
    patId = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    gender = serializers.CharField(max_length=255)
    dob = serializers.CharField(max_length=255)
    medSvcCode = serializers.CharField(max_length=255)
    icd10Code = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    serviceDate = serializers.CharField(max_length=255)
    serviceProviderRankingId = serializers.CharField(max_length=255)
    visitType = serializers.CharField(max_length=255)


class IncomingServicesReceivedSerializer(serializers.Serializer):
    messageType = serializers.CharField(max_length=255)
    orgName = serializers.CharField(max_length=255)
    facilityHfrCode = serializers.CharField(max_length=255)
    items = IncomingServiceReceivedItemsSerializer(many=True, read_only=False)


class DeathByDiseaseCaseAtFacilityItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.DeathByDiseaseCaseAtFacilityItems
        fields = ('death_by_disease_case_at_facility','ward_name','ward_id','patient_id',
                  'gender','date_of_birth','icd_10_code','date_death_occurred')


class DeathByDiseaseCaseAtFacilitySerializer(serializers.ModelSerializer):
    items = DeathByDiseaseCaseAtFacilityItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.DeathByDiseaseCaseAtFacility
        fields = ('org_name', 'facility_hfr_code', 'items')


class IncomingDeathByDiseaseCaseAtTheFacilityItemsSerializer(serializers.Serializer):
    wardId = serializers.CharField(max_length=255)
    wardName = serializers.CharField(max_length=255)
    patId = serializers.CharField(max_length=255)
    icd10Code = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    gender = serializers.CharField(max_length=255)
    dob = serializers.CharField(max_length=255)
    dateDeathOccurred = serializers.CharField(max_length=255)


class IncomingDeathByDiseaseCaseAtTheFacilitySerializer(serializers.Serializer):
    messageType = serializers.CharField(max_length=255)
    orgName = serializers.CharField(max_length=255)
    facilityHfrCode = serializers.CharField(max_length=255)
    items = IncomingDeathByDiseaseCaseAtTheFacilityItemsSerializer(many=True, read_only=False)


class DeathByDiseaseCaseNotAtFacilityItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.DeathByDiseaseCaseNotAtFacilityItems
        fields = ('place_of_death_id','gender','date_of_birth','icd_10_code','date_death_occurred','death_id')


class DeathByDiseaseCaseNotAtFacilitySerializer(serializers.ModelSerializer):
    items = DeathByDiseaseCaseNotAtFacilityItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.DeathByDiseaseCaseNotAtFacility
        fields = ('org_name', 'facility_hfr_code', 'items')


class IncomingDeathByDiseaseCaseNotAtTheFacilityItemsSerializer(serializers.Serializer):
    deathId = serializers.CharField(max_length=255)
    placeOfDeathId = serializers.CharField(max_length=255)
    icd10Code = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True )
    gender = serializers.CharField(max_length=255)
    dob = serializers.CharField(max_length=255)
    dateDeathOccurred = serializers.CharField(max_length=255)


class IncomingDeathByDiseaseCaseNotAtTheFacilitySerializer(serializers.Serializer):
    messageType = serializers.CharField(max_length=255)
    orgName = serializers.CharField(max_length=255)
    facilityHfrCode = serializers.CharField(max_length=255)
    items = IncomingDeathByDiseaseCaseNotAtTheFacilityItemsSerializer(many=True, read_only=False)


class BedOccupancyItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.BedOccupancyItems
        fields = ('bed_occupancy','patient_id','admission_date','discharge_date','ward_name','ward_id')


class BedOccupancySerializer(serializers.ModelSerializer):
    items = BedOccupancyItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.BedOccupancy
        fields = ('org_name', 'facility_hfr_code', 'items')


class IncomingBedOccupancyItemsSerializer(serializers.Serializer):
    wardId = serializers.CharField(max_length=255)
    wardName = serializers.CharField(max_length=255)
    patId = serializers.CharField(max_length=255)
    admissionDate = serializers.CharField(max_length=255)
    dischargeDate = serializers.CharField(max_length=255)


class IncomingBedOccupancySerializer(serializers.Serializer):
    messageType = serializers.CharField(max_length=255)
    orgName = serializers.CharField(max_length=255)
    facilityHfrCode = serializers.CharField(max_length=255)
    items = IncomingBedOccupancyItemsSerializer(many=True, read_only=False)


class RevenueReceivedItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.RevenueReceivedItems
        fields = ('revenue_received','system_trans_id','transaction_date','patient_id', 'gender','date_of_birth',
                  'med_svc_code', 'payer_id','exemption_category_id','billed_amount','waived_amount','service_provider_ranking_id')


class RevenueReceivedSerializer(serializers.ModelSerializer):
    items = RevenueReceivedItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.RevenueReceived
        fields = ('org_name', 'facility_hfr_code', 'items')


class IncomingRevenueReceivedItemsSerializer(serializers.Serializer):
    systemTransId = serializers.CharField(max_length=255)
    transactionDate = serializers.CharField(max_length=255)
    patId = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    gender = serializers.CharField(max_length=255)
    dob = serializers.CharField(max_length=255,required=False, allow_blank=True, allow_null=True)
    medSvcCode = serializers.CharField(max_length=255)
    payerId = serializers.CharField(max_length=255)
    exemptionCategoryId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    billedAmount = serializers.IntegerField()
    waivedAmount = serializers.IntegerField()
    serviceProviderRankingId = serializers.CharField(max_length=255)


class IncomingRevenueReceivedSerializer(serializers.Serializer):
    messageType = serializers.CharField(max_length=255)
    orgName = serializers.CharField(max_length=255)
    facilityHfrCode = serializers.CharField(max_length=255)
    items = IncomingRevenueReceivedItemsSerializer(many=True, read_only=False)


class ICD10SubCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = terminology_services_management.ICD10SubCode
        fields = ('id','sub_code', 'description')


class ICD10CodeSerializer(serializers.ModelSerializer):
    sub_code =  ICD10SubCodeSerializer(many=True, read_only=False)

    class Meta:
        model = terminology_services_management.ICD10Code
        fields = ('id','code', 'description', 'sub_code')


class ICD10CodeSubCategorySerializer(serializers.ModelSerializer):
    code = ICD10CodeSerializer(many=True, read_only=False)

    class Meta:
        model = terminology_services_management.ICD10CodeSubCategory
        fields = ['id', 'description','code']


class ICD10CodeCategorySerializer(serializers.ModelSerializer):
    sub_category = ICD10CodeSubCategorySerializer(many=True, read_only=False)

    class Meta:
        model = terminology_services_management.ICD10CodeCategory
        fields = ('id', 'description', 'sub_category')


class CPTCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = terminology_services_management.CPTCode
        fields = ('id','code','description')


class CPTCodeSubCategorySerializer(serializers.ModelSerializer):
    code = CPTCodeSerializer(many=True, read_only=False)

    class Meta:
        model = terminology_services_management.CPTCodeSubCategory
        fields = ('id','description', 'code')


class CPTCodeCategorySerializer(serializers.ModelSerializer):
    sub_category = CPTCodeSubCategorySerializer(many=True, read_only=False)

    class Meta:
        model = terminology_services_management.CPTCodeCategory
        fields = ('id', 'description', 'sub_category')


class IncomingClaimsSerializer(serializers.Serializer):
    facilityHfrCode = serializers.CharField(max_length=255)
    claimedAmount = serializers.DecimalField(max_digits=10, decimal_places=2)
    period = serializers.CharField(max_length=255)
    computedAmount = serializers.DecimalField(max_digits=10, decimal_places=2)
    acceptedAmount = serializers.DecimalField(max_digits=10, decimal_places=2)
    loanDeductions = serializers.DecimalField(max_digits=10, decimal_places=2)
    otherDeductions = serializers.DecimalField(max_digits=10, decimal_places=2)
    paidAmount = serializers.DecimalField(max_digits=10, decimal_places=2)


class ClaimsSerializer(serializers.ModelSerializer):

    class Meta:
        model = nhif_models.Claims
        fields = ('id', 'claimed_amount', 'period', 'computed_amount', 'accepted_amount', 'loan_deductions',
                  'other_deductions', 'paid_amount')