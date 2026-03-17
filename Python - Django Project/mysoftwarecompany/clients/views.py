from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail
from .models import Company, Employee
from .forms import ContactForm, CompanyForm, EmployeeForm

# Create your views here.
def list_companies(request):
    companies = Company.objects.all()
    return render(request, 'clients/companies_list.html', {'companies' : companies})

def company_detail(request, company_id):
    company = get_object_or_404(Company, id = company_id)
    return render(request, 'clients/company_detail.html', {'company' : company})

def employees_search(request, company_id):
    query = request.GET.get('q', '')
    company = get_object_or_404(Company, id = company_id)

    if query:
        employees = company.employees.filter(Q(first_name__icontains = query) | Q(last_name__icontains = query))
    else:
        employees = Employee.objects.none()
    template_data = {
        'company' : company,
        'query' : query,
        'employees' : employees
    }
    return render(request, 'clients/employees_search_results.html', template_data)
def contact_us(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request,'clients/contact_us.html', { "form" : form })
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            send_mail(subject =  f"New contact us message From {name}", message = message, from_email = email, recipient_list = ["admin@softwarecompany.com"],)

            return render(request,'clients/contact_us.html', { "form" : ContactForm(), "success" : True })
        else:
            return render(request,'clients/contact_us.html', { "form" : form, "success" : False })
def create_company(request):
    if request.method =="GET":
        form = CompanyForm()
        return render(request, 'clients/create_company.html', {"form" : form })
    elif request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            company = form.instance
            post_data = {"form": CompanyForm(), "new_company" : company}
            return render(request, 'clients/create_company.html', post_data)
        else:
            return render(request, 'clients/create_company.html', {"form" : form })
def update_company(request, company_id):
    company = get_object_or_404(Company, id = company_id)
    if request.method == "GET":
        form = CompanyForm(instance = company)
        get_data = {"form": form, "company" : company}
        return render(request, 'clients/update_company.html', get_data)
    elif request.method == "POST":
        form = CompanyForm(request.POST, instance = company)
        if form.is_valid():
            form.save()

            updated_company = form.instance
            post_data = {"form": CompanyForm(instance = updated_company), "company" : company, "success": True}
            return render(request, 'clients/update_company.html', post_data)
        else:
            return render(request, 'clients/update_company.html', {"form" : form })
def add_company_employee(request, company_id):
    company = get_object_or_404(Company, id = company_id)
    if request.method == "GET":
        form = EmployeeForm
        get_data = {"form": form, "company" : company}
        return render(request, 'clients/add_company_employee.html', get_data)
    elif request.method =="POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            new_employee = form.save(commit = False)
            new_employee.company = company
            new_employee.save()

            post_data = {"form" : EmployeeForm(), "company" : company, "employee" : new_employee, "success": True}
            return render(request, 'clients/add_company_employee.html', post_data)
        else:
            post_data = {"form" : form, "company" : company}
            return render(request, 'clients/add_company_employee.html', post_data)