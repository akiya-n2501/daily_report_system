from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy

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


@method_decorator(staff_member_required, name="dispatch")
class EmployeeListView(ListView):
    model = Employee
    template_name = "employees/employee_list.html"
    context_object_name = "employee"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.select_related("user").values("is_staff")
        return context


@method_decorator(staff_member_required, name="dispatch")
class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = "employees/employee_form_edit.html"
    form_class = EmployeeUserForm
    success_url = reverse_lazy('employees:employee_edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.select_related("user").values("is_staff")
        return context


# TODO Email, Username, Passwordを変更可能にする。
# @staff_member_required
# def employee_edit(request, pk):
#     employee = get_object_or_404(Employee, pk=pk)
#     return render(request, "employees/employee_edit.html", {"employee": employee})


# @staff_member_required
# def employee_update(request, pk):
#     employee = get_object_or_404(Employee, pk=pk)
#     if request.method == "POST":
#         employee.name = request.POST["name"]
#         employee.email = request.POST["email"]
#         employee.save()
#         return redirect("employee_index")
#     return redirect("employee_edit", pk=pk)


@staff_member_required
def employee_delete_confirm(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(
        request, "employees/employee_delete_confirm.html", {"employee": employee}
    )


@staff_member_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect("employee_index")
