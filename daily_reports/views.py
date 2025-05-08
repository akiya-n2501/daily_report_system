from django.views.generic import CreateView, ListView
from django.shortcuts import render
from .forms import DailyReportForm

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
    
class DailyReportCreateView(CreateView):
    model = DailyReport
    form_class = DailyReportForm
    
    template_name = "daily_reports/daily_report_new.html"
    success_url = "daily_reports/new/"
# success_url 変更する必要あり