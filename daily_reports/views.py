from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DailyReport, Employee
from django.urls import reverse_lazy
from .forms import DailyReportForm

# 日報一覧
class DailyReportListView(ListView):
    model = DailyReport
    template_name = "daily_reports/daily_report_list.html"
    context_object_name = "daily_reports"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = Employee.objects.select_related("employee_code").values(
            "name"
        )
        return context


# 日報編集画面
class DailyReportEditView(LoginRequiredMixin, UpdateView):
    model = DailyReport
    form_class = DailyReportForm
    template_name = 'daily_reports/daily_report_edit.html'

    success_url = reverse_lazy('daily_reports:daily_report_detail')
    def get_context_data(self, **kwargs):
       context = super(DailyReportEditView, self).get_context_data(**kwargs)
       context['message_type'] = "edit"
       return context