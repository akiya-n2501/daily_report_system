from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.urls import reverse_lazy
from employees.models import Employee
from .models import DailyReport, DailyReportComment
from .forms import DailyReportCommentForm


@method_decorator(staff_member_required, name="dispatch")
class DailyReportCommentCreateView(CreateView):
    model = DailyReportComment
    template_name = "daily_reports/daily_reports_comment_new.html"
    form_class = DailyReportCommentForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        daily_report = get_object_or_404(DailyReport, id=self.kwargs.get("report_id"))
        employee = Employee.objects.get(user=self.request.user)

        form.instance.employee_code = employee
        form.instance.daily_report_code = daily_report
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        daily_report = get_object_or_404(DailyReport, id=self.kwargs.get("report_id"))

        context = super().get_context_data(**kwargs)
        context["employee_name"] = daily_report.employee_code.name
        context["reported_on"] = daily_report.reported_on
        context["job_description"] = daily_report.job_description
        return context
