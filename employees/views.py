from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Employee


def home(request):
    return render(request, "home.html")


@login_required
def employee_create(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        Employee.objects.create(name=name, email=email)
        return redirect("employee_index")
    return redirect("employee_new")


@login_required
def employee_new(request):
    return render(request, "employees/employee_new.html")


@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, "employees/employee_list.html", {"employees": employees})


@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, "employees/employee_edit.html", {"employee": employee})


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.name = request.POST["name"]
        employee.email = request.POST["email"]
        employee.save()
        return redirect("employee_index")
    return redirect("employee_edit", pk=pk)


@login_required
def employee_delete_confirm(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, "employees/employee_delete.html", {"employee": employee})


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect("employee_index")
