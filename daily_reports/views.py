from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import ListView
from django.urls import reverse
from employees.models import Employee
from .models import DailyReport, DailyReportComment
from .forms import DailyReportCommentForm


# 日報コメント新規作成画面
@method_decorator(staff_member_required, name="dispatch")
class DailyReportCommentCreateView(CreateView):
    model = DailyReportComment
    template_name = "daily_reports/daily_reports_comment_new.html"
    form_class = DailyReportCommentForm

    def form_valid(self, form):
        daily_report = get_object_or_404(DailyReport, id=self.kwargs.get("report_id"))
        employee = Employee.objects.get(user=self.request.user)

        # formのインスタンスにemployeeとdaily_reportを設定
        form.instance.employee_code = employee
        form.instance.daily_report_code = daily_report
        return super().form_valid(form)

    # テンプレートで利用するためのコンテキストの設定
    def get_context_data(self, **kwargs):
        daily_report = get_object_or_404(DailyReport, id=self.kwargs.get("report_id"))

        context = super().get_context_data(**kwargs)
        context["employee_name"] = daily_report.employee_code.name
        context["reported_on"] = daily_report.reported_on
        context["job_description"] = daily_report.job_description
        return context

    # 成功時のURLをpkから設定
    def get_success_url(self):
        return reverse(
            "daily_report_detail", kwargs={"report_id": self.kwargs.get("report_id")}
        )


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
