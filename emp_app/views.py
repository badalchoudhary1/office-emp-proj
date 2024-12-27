from django.shortcuts import HttpResponse
from .models import Role,Department,Employee
from datetime import datetime
from django.shortcuts import render
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request,'index.html')


def all_emp(request):
    emps=Employee.objects.all()
    context={
        'emps':emps

    }
    print(context)
    return render(request,'view_all_emp.html',context)


def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST.get('salary', 0))
        bonus = int(request.POST.get('bonus', 0))
        phone = int(request.POST.get('phone', 0))
        dept = int(request.POST.get('dept', 0))
        role = int(request.POST.get('role', 0))
        
        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            dept_id=dept,
            role_id=role,
            hire_date=datetime.now(),
            phone=phone
        )
        new_emp.save()
        return HttpResponse("Employee added successfully")
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("Invalid request method")

def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed=Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully")
        except:
            return HttpResponse("Employee not found")
    emps=Employee.objects.all()
    context={
        'emps':emps

    }
    return render(request,'remove_emp.html',context)


def filter_emp(request):
    if request.method =='POST':
        name=request.POST['name']
        dept=request.POST['dept']
        role=request.POST['role']
        emps=Employee.objects.all()
        if name:
            emps=emps.filter(Q(first_name__icontains=name)|Q(last_name__icontains=name))
        if dept:
            emps=emps.filter(dept__name=dept)
        if role:
            emps=emps.filter(role__name=role)
        context = {
            'emps': emps,
            # 'name': name,
            # 'dept': dept,
            # 'role': role,
        }

        return render(request, 'view_all_emp.html', context)
    
    return render(request, 'filter_emp.html')