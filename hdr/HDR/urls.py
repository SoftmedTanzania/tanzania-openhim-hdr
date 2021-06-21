
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
from MasterData import views as master_data_views
from Core import tasks as core_tasks

urlpatterns = [
    path('', include('UserManagement.urls')),
    path('admin/', admin.site.urls),
    path('get_', include('MasterData.urls')),
    path('api_', include('API.urls')),
    path('insert_icd_10', master_data_views.import_icd_10_codes, name='insert_icd_10'),
    path('save_payload_from_csv', core_tasks.save_payload_from_csv, name='save_payload_from_csv')

]
