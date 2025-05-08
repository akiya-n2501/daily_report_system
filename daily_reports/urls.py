from django.urls import path

# from . import views
from .views import DailyReportListView, DailyReportEditView

urlpatterns = [
    path("", DailyReportListView.as_view(), name="daily_report_index"),
    path("<int:pk>/edit/", DailyReportEditView.as_view(), name="daily_report_edit"),
]
