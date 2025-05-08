from django.urls import path

from . import views

from .views import DailyReportListView, DailyReportCreateView

urlpatterns = [
    path("", DailyReportListView.as_view(), name="daily_report_index"),
    path("new/", DailyReportCreateView.as_view(),name="daily_report_new"),
]