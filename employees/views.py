from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import EmployeeUserForm, EmployeeUserEditForm
from .models import Employee


@login_required
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


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class EmployeeListView(ListView):
    model = Employee
    template_name = "employees/employee_list.html"
    context_object_name = "employee"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = "employees/employee_form_edit.html"
    form_class = EmployeeUserEditForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_instance'] = self.get_object().user
        return kwargs

    def get_success_url(self):
        return reverse('employee_index')


@login_required
@staff_member_required
def employee_delete_confirm(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(
        request, "employees/employee_delete_confirm.html", {"employee": employee}
    )


@login_required
@staff_member_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect("employee_index")
