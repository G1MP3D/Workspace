from django.urls import path
from .views import list_companies, company_detail, employees_search, contact_us, create_company, update_company, add_company_employee

urlpatterns = [
    path('companies/', list_companies, name='companies_list'), 
    path('company/<int:company_id>', company_detail, name = 'company_detail'),
    path('company/create/', create_company, name = 'create_company'),
    path('company/<int:company_id>/update', update_company, name = 'update_company'),
    path('company/<int:company_id>/employees/search', employees_search, name = 'employees_search'),
    path('company/<int:company_id>/employees/add', add_company_employee, name = 'add_company_employee'),
    path('contact/', contact_us, name = "contact_us"),
]