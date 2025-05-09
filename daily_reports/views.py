from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django.views.generic import CreateView, ListView, UpdateView

from .forms import DailyReportCommentForm, DailyReportForm, DailyReportSearchForm
from .models import DailyReport, DailyReportComment, Employee


# 日報コメント新規作成画面
@method_decorator(login_required, name="dispatch")
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


# 日報新規登録
@method_decorator(login_required, name="dispatch")
class DailyReportCreateView(CreateView):
    model = DailyReport
    form_class = DailyReportForm

    template_name = "daily_reports/daily_report_new.html"

    def get_success_url(self):
        return reverse(
            "daily_report_index",
        )


# 日報検索
@method_decorator(login_required, name="dispatch")
class DailyReportSearchView(ListView):
    model = DailyReport
    template_name = "daily_reports/daily_report_list.html"
    context_object_name = "daily_reports"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = Employee.objects.select_related("employee_code").values(
            "name"
        )
        context["form"] = DailyReportSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = DailyReportSearchForm(self.request.GET)

        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")

            # 検索
            if keyword:
                queryset = queryset.filter(
                    job_description__icontains=keyword
                ) | queryset.filter(employee_code__name__icontains=keyword)
            if start_date and end_date:
                queryset = queryset.filter(
                    reported_on__range=(
                        make_aware(datetime.combine(start_date, datetime.min.time())),
                        make_aware(datetime.combine(end_date, datetime.max.time())),
                    )
                )
            elif start_date:
                queryset = queryset.filter(
                    reported_on__gte=make_aware(
                        datetime.combine(start_date, datetime.min.time())
                    )
                )
            elif end_date:
                queryset = queryset.filter(
                    reported_on__lte=make_aware(
                        datetime.combine(end_date, datetime.max.time())
                    )
                )
            return queryset

# 日報の編集
@method_decorator(login_required, name="dispatch")
class DailyReportEditView(LoginRequiredMixin, UpdateView):
    model = DailyReport
    form_class = DailyReportForm
    template_name = 'daily_reports/daily_report_edit.html'

    success_url = reverse_lazy('daily_reports:daily_report_detail')
    def get_context_data(self, **kwargs):
       context = super(DailyReportEditView, self).get_context_data(**kwargs)
       context['message_type'] = "edit"
       return context