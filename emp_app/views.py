from django.shortcuts import HttpResponse
from .models import Role,Department,Employee
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def index(request):
    return render(request,'index.html')

@login_required
def all_emp(request):
    emps=Employee.objects.all()
    context={
        'emps':emps

    }
    print(context)
    return render(request,'view_all_emp.html',context)

@login_required
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
@login_required
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

@login_required
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


# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')
