from django.urls import path

from . import views
# from .views import DailyReportCreateview

urlpatterns = [
    # path("new/",DailyReportCreateview.as_view(),name="daily_report_new"),
    # 候補　name = ("dairy_report_create")
    path("new/", views.daily_report_new, name="daily_report_new"),
]