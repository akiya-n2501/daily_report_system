from django.urls import path

# from . import views
from .views import DailyReportEditView

urlpatterns = [
    path("<int:pk>/edit/", DailyReportEditView.as_view(), name="daily_report_edit"),
]
