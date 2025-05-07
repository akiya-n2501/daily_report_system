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

    success_url = reverse_lazy('daily_reports:daily_report_detail')
    def get_context_data(self, **kwargs):
       context = super(DailyReportEditView, self).get_context_data(**kwargs)
       context['message_type'] = "edit"
       return context