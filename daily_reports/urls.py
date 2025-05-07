from django.urls import path

from .views import DailyReportListView

urlpatterns = [
    path("", DailyReportListView.as_view(), name="daily_report_index"),
]
