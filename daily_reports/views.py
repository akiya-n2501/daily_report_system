from django.shortcuts import render
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DailyReport
from django.urls import reverse_lazy
from .forms import DailyReportForm

class DailyReportEditView(LoginRequiredMixin, UpdateView):
    model = DailyReport
    form_class = DailyReportForm
    template_name = 'daily_reports/daily_report_edit.html'
from django.views.generic import ListView

from .models import DailyReport, Employee


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

    success_url = reverse_lazy('daily_reports:daily_report_detail')
    def get_context_data(self, **kwargs):
       context = super(DailyReportEditView, self).get_context_data(**kwargs)
       context['message_type'] = "edit"
       return context