from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import DailyReport, Employee


# 日報一覧
@method_decorator(login_required, name="dispatch")
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
