from django.urls import path
from UserManagement.views import main
from Core import views as core_views

urlpatterns = [
    path('', main.get_login_page, name='login_page'),
    path('admin', main.get_admin_page, name= 'admin'),
    path('password/', main.change_password, name='change_password'),
    path('dashboard', main.get_dashboard, name='dashboard'),
    path('get_transaction_summary_lines/<int:item_pk>/', main.get_transaction_summary_lines, name='get_transaction_summary_lines'),
    path('save_changed_password/', main.set_changed_password, name='save_changed_password'),
    path('user', main.authenticate_user, name='authenticate_user'),
    path('accounts/login/', main.change_password, name='login_required_page'),
    path('logout', main.logout_view, name='logout'),
    path('get_audit_report/<int:item_pk>/', main.get_audit_report, name='get_audit_report'),
    path('get_remove_transaction/<int:item_pk>/', main.remove_transaction, name='get_remove_transaction'),
    path('change_password', main.change_password, name='change_password'),
    path('export_transaction_lines', core_views.convert_to_csv, name='export_transaction_lines'),
    path('upload_payload', core_views.upload_payload, name='upload_payload'),
    path('upload_cpt_codes', core_views.upload_cpt_codes, name='upload_cpt_codes'),
    path('download_cpt_codes_as_csv', core_views.download_cpt_codes_as_csv, name='download_cpt_codes_as_csv'),
    path('filter_transaction_lines', core_views.filter_transaction_lines, name='filter_transaction_lines'),


]