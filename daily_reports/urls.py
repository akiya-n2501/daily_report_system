from django.urls import path

from .views import (
    DailyReportCommentCreateView,
    DailyReportListView,
    DailyReportSearchView,
    DailyReportCreateView
)

urlpatterns = [
    path(
        "<int:report_id>/comment/new/",
        DailyReportCommentCreateView.as_view(),
        name="daily_report_comment_new",
    ),
    path(
        "<int:report_id>/detail/",
        DailyReportListView.as_view(),
        name="daily_report_detail",
    ),
    path("", DailyReportListView.as_view(), name="daily_report_index"),
    path("search_list/", DailyReportSearchView.as_view(), name="search_list"),
    path("new/", DailyReportCreateView.as_view(),name="daily_report_new")
]