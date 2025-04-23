from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeUserForm
from .models import Employee


def home(request):
    return render(request, "home.html")


@staff_member_required
def employee_new(request):
    if request.method == "POST":
        form = EmployeeUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("employee_index")
    else:
        form = EmployeeUserForm()
    return render(request, "employees/employee_form.html", {"form": form})


@staff_member_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, "employees/employee_list.html", {"employees": employees})


# TODO Email, Username, Passwordを変更可能にする。
@staff_member_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, "employees/employee_edit.html", {"employee": employee})


@staff_member_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.name = request.POST["name"]
        employee.email = request.POST["email"]
        employee.save()
        return redirect("employee_index")
    return redirect("employee_edit", pk=pk)


@staff_member_required
def employee_delete_confirm(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, "employees/employee_delete.html", {"employee": employee})


@staff_member_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect("employee_index")
