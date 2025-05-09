from django.urls import path

from .views import (
    DailyReportCommentCreateView,
    DailyReportCreateView,
    DailyReportDeleteView,
    DailyReportDetailView,
    DailyReportEditView,
    DailyReportListView,
    daily_report_delete_confirm,
)

urlpatterns = [
    path(
        "<int:pk>/comment/new/",
        DailyReportCommentCreateView.as_view(),
        name="daily_report_comment_new",
    ),
    path(
        "<int:pk>/detail/",
        DailyReportDetailView.as_view(),
        name="daily_report_detail",
    ),
    path("", DailyReportListView.as_view(), name="daily_report_index"),
    path("new/", DailyReportCreateView.as_view(), name="daily_report_new"),
    path("<int:pk>/edit/", DailyReportEditView.as_view(), name="daily_report_edit"),
    path(
        "<int:pk>/delete_confirm/",
        daily_report_delete_confirm,
        name="daily_report_delete_confirm",
    ),
    path(
        "<int:pk>/delete/", DailyReportDeleteView.as_view(), name="daily_report_delete"
    ),
]
