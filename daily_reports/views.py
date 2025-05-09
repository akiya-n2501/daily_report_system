from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    DailyReportCommentForm,
    DailyReportEditForm,
    DailyReportForm,
    DailyReportSearchForm,
)
from .models import DailyReport, DailyReportComment, Employee


# 日報コメント新規作成画面
@method_decorator(login_required, name="dispatch")
class DailyReportCommentCreateView(CreateView):
    model = DailyReportComment
    template_name = "daily_reports/daily_reports_comment_new.html"
    form_class = DailyReportCommentForm

    def form_valid(self, form):
        daily_report = get_object_or_404(DailyReport, id=self.kwargs.get("pk"))
        employee = Employee.objects.get(user=self.request.user)

        # formのインスタンスにemployeeとdaily_reportを設定
        form.instance.employee_code = employee
        form.instance.daily_report_code = daily_report
        return super().form_valid(form)

    # テンプレートで利用するためのコンテキストの設定
    def get_context_data(self, **kwargs):
        daily_report = get_object_or_404(DailyReport, id=self.kwargs.get("pk"))

        context = super().get_context_data(**kwargs)
        context["employee_name"] = daily_report.employee_code.name
        context["reported_on"] = daily_report.reported_on
        context["daily_report"] = daily_report
        context["job_description"] = daily_report.job_description
        return context

    # 成功時のURLをpkから設定
    def get_success_url(self):
        return reverse("daily_report_detail", kwargs={"pk": self.kwargs.get("pk")})


# 日報新規登録
@method_decorator(login_required, name="dispatch")
class DailyReportCreateView(CreateView):
    model = DailyReport
    form_class = DailyReportForm
    template_name = "daily_reports/daily_report_new.html"

    def form_valid(self, form):
        if not form.instance.reported_on:
            form.instance.reported_on = timezone.now().date()  # 今日の日付を設定
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['reported_on'] = timezone.now().date()  # 今日の日付を初期値に設定
        initial["employee_code"] = Employee.objects.get(user=self.request.user)
        initial["reported_on"] = timezone.now().date()  # 今日の日付を初期値に設定
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee_code"] = Employee.objects.get(user=self.request.user)
        return context

    def get_success_url(self):
        return reverse(
            "daily_report_index",
        )


# 日報一覧画面 検索機能あり
@method_decorator(login_required, name="dispatch")
class DailyReportListView(ListView):
    model = DailyReport
    template_name = "daily_reports/daily_report_list.html"
    context_object_name = "daily_reports"
    ordering = "-reported_on"

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


# 日報編集画面
@method_decorator(login_required, name="dispatch")
class DailyReportEditView(UpdateView):
    model = DailyReport
    form_class = DailyReportEditForm
    template_name = "daily_reports/daily_report_edit.html"

    # success_url = reverse_lazy('daily_report_detail', kwargs={"pk": self.kwargs.get("pk")})
    def get_context_data(self, **kwargs):
        daily_report = get_object_or_404(DailyReport, id=self.kwargs.get("pk"))

        context = super(DailyReportEditView, self).get_context_data(**kwargs)
        context["message_type"] = "edit"
        context["obj"] = DailyReport.objects.get(id=self.kwargs["pk"])
        context["employee_name"] = daily_report.employee_code.name
        context["reported_on"] = daily_report.reported_on
        return context

    # 成功時のURLをpkから設定
    def get_success_url(self):
        return reverse("daily_report_detail", kwargs={"pk": self.kwargs.get("pk")})


# 日報詳細画面
@method_decorator(login_required, name="dispatch")
class DailyReportDetailView(DetailView):
    model = DailyReport
    template_name = "daily_reports/daily_report_detail.html"
    context_object_name = "daily_report"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = Employee.objects.select_related("employee_code").values(
            "name"
        )
        # FKの無い側からある側にモデルを逆参照
        context["obj"] = DailyReport.objects.get(id=self.kwargs["pk"])
        return context


# 日報削除確認画面
@login_required
def daily_report_delete_confirm(request, pk):
    daily_report = get_object_or_404(DailyReport, pk=pk)
    return render(
        request,
        "daily_reports/daily_report_delete_confirm.html",
        {"daily_report": daily_report},
    )


# 日報削除
@method_decorator(staff_member_required, name="dispatch")
class DailyReportDeleteView(DeleteView):
    model = DailyReport
    template_name = "daily_reports/daily_report_delete_confirm.html"
    success_url = reverse_lazy("daily_report_index")
