from django.urls import path

from .views import DailyReportListView, DailyReportSearchView

urlpatterns = [
    path("", DailyReportListView.as_view(), name="daily_report_index"),
    path("search_list/", DailyReportSearchView.as_view(), name="search_list"),
]
