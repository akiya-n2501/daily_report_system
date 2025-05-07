from django.views.generic import CreateView
from .models import DailyReport
from django.shortcuts import render

# Create your views here.
# class DailyReportCreateView(CreateView):
    # model = DailyReport
    # fields = ["job_description","reported_on"]
    # # created_atは必要か
    # template_name = "daily_repots/daily_reports_new.html"

def daily_report_new(request):

    return render(request, "daily_reports/daily_report_new.html" )
