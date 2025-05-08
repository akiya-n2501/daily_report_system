from django.contrib.auth.decorators import login_required
from django.db.models import Q
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


# @method_decorator(login_required, name="dispatch")
class DailyReportSearchView(ListView):
    model = DailyReport
    template_name = "daily_reports/daily_report_list.html"
    context_object_name = "daily_reports"

    def get_queryset(self):
        # 検索
        query = self.request.GET.get("q", None)
        if query:
            results = DailyReport.objects.filter(
                Q(job_description__icontains=query)
                | Q(employee_code__name__icontains=query)
            )
        else:
            results = DailyReport.objects.all()

        # 日付範囲
        date_min = self.request.GET.get("date_min")
        date_max = self.request.GET.get("date_max")
        if date_min and date_max:
            results = DailyReport.objects.filter(
                reported_on__range=[date_min, date_max]
            ).order_by("reported_on")
        elif date_min:
            results = DailyReport.objects.filter(reported_on__gte=date_min).order_by(
                "reported_on"
            )
        elif date_max:
            results = DailyReport.objects.filter(reported_on__lte=date_max).order_by(
                "reported_on"
            )
        else:
            results = DailyReport.objects.filter(reported_on__isnull=True)

        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = Employee.objects.select_related("employee_code").values(
            "name"
        )
        return context
