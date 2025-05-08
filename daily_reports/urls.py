from django.urls import path

from . import views
from .views import DailyReportCommentCreateView
from .views import DailyReportListView

urlpatterns = [
    path(
        "<int:report_id>/comment/new/",
        DailyReportCommentCreateView.as_view(),
        name="daily_report_comment_new",
    ),
    path("", DailyReportListView.as_view(), name="daily_report_index"),
]
