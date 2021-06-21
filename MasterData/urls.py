from django.urls import path
from MasterData import views

urlpatterns = [
    path('departments', views.get_departments_page, name='get_departments_page'),
    path('exemptions', views.get_exemptions_page, name='get_exemptions_page'),
    path('payers', views.get_payers_page, name='get_payers_page'),
    path('wards', views.get_wards_page, name='get_wards_page'),
    path('gender', views.get_gender_page, name='get_gender_page'),
    path('places_of_death', views.get_places_of_death_page, name='get_places_of_death_page'),
    path('service_provider_rankings', views.get_service_provider_rankings_page, name='get_service_provider_rankings_page'),
    path('delete_mapping', views.delete_mapping, name='delete_mapping'),
    path('cpt_codes_page', views.get_cpt_codes_page, name='cpt_codes_page'),
    path('update_ward/<int:item_pk>/', views.update_ward, name='update_ward'),
    path('update_department/<int:item_pk>/', views.update_department, name='update_department'),
    path('update_exemption/<int:item_pk>/', views.update_exemption, name='update_exemption'),
    path('update_payer/<int:item_pk>/', views.update_payer, name='update_payer'),
    path('update_gender/<int:item_pk>/', views.update_gender, name='update_gender'),
    path('update_place_of_death/<int:item_pk>/', views.update_place_of_death, name='update_place_of_death'),
    path('update_service_provider_ranking/<int:item_pk>/', views.update_service_provider_ranking, name='update_service_provider_ranking'),
    path('update_cpt_code/<int:item_pk>/', views.update_cpt_code, name='update_cpt_code'),

]