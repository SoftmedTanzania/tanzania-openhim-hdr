
"""
HDR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))."""

from django.contrib import admin
from django.urls import path, include
from UserManagement.views import main as user_management_views
from Core import tasks as core_tasks
from DHIS import tasks as dhis_tasks

urlpatterns = [

    # path('', include('UserManagement.urls')),
    path("", include(("UserManagement.urls", "user_management"), namespace="user_management")),

    # path('authenticate', api_views.authenticate_user, name='authenticate'),
    path('admin/', admin.site.urls),
    path('get_', include('MasterData.urls')),
    path('api_', include('API.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('change_password', user_management_views.change_password, name="change_password"),
    path('calculate_and_save_bed_occupancy_rate', core_tasks.calculate_and_save_bed_occupancy_rate,
         name='calculate_and_save_bed_occupancy_rate'),
    path('create_claims_payload', dhis_tasks.create_claims_payload, name='create_claims_payload'),
    path('create_death_payload', dhis_tasks.create_death_payload, name='create_death_payload'),
    path('save_payload_from_csv', core_tasks.save_payload_from_csv, name='save_payload_from_csv'),

]
