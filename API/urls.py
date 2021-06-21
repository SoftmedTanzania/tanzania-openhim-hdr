from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('transactions_summary', views.TransactionSummaryView)
router.register('services_received', views.ServiceReceivedView)
router.register('death_by_disease_cases_at_facility', views.DeathByDiseaseCaseAtFacilityView)
router.register('death_by_disease_cases_not_at_facility', views.DeathByDiseaseCaseNotAtFacilityView)
router.register('bed_occupancy', views.BedOccupancyView)
router.register('revenue_received', views.RevenueReceivedView)


urlpatterns = [
    path('', include(router.urls)),
]